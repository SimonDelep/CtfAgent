"""Client LLM minimal, OpenAI-compatible (vLLM), sans dépendance au SDK openai.

On parle directement au endpoint /chat/completions via `requests`. Tout modèle servi
par vLLM avec --enable-auto-tool-choice expose le function-calling au format OpenAI ;
on reste donc agnostique au modèle (Qwen, Llama, DeepSeek, ...).
"""
from __future__ import annotations

import json
import time
from dataclasses import dataclass, field
from typing import Any

import requests


@dataclass
class LLMUsage:
    prompt_tokens: int = 0
    completion_tokens: int = 0
    total_tokens: int = 0

    def add(self, other: "LLMUsage") -> None:
        self.prompt_tokens += other.prompt_tokens
        self.completion_tokens += other.completion_tokens
        self.total_tokens += other.total_tokens


@dataclass
class LLMResponse:
    content: str | None
    tool_calls: list[dict]            # [{id, name, arguments(dict)}]
    finish_reason: str
    usage: LLMUsage
    thought: str | None = None        # texte de raisonnement à AFFICHER (hors JSON d'appel)
    raw: dict = field(default_factory=dict)


class LLMClient:
    def __init__(self, cfg: dict):
        llm = cfg["llm"]
        self.base_url = llm["base_url"].rstrip("/")
        self.api_key = llm.get("api_key", "EMPTY")
        self.model = llm["model"]
        self.temperature = float(llm.get("temperature", 0.2))
        self.max_tokens = int(llm.get("max_tokens", 4096))
        self.timeout = int(llm.get("request_timeout", 300))
        self.total_usage = LLMUsage()

    def chat(
        self,
        messages: list[dict],
        tools: list[dict] | None = None,
        temperature: float | None = None,
        max_retries: int = 3,
    ) -> LLMResponse:
        payload: dict[str, Any] = {
            "model": self.model,
            "messages": messages,
            "temperature": self.temperature if temperature is None else temperature,
            "max_tokens": self.max_tokens,
        }
        if tools:
            payload["tools"] = tools
            payload["tool_choice"] = "auto"

        url = f"{self.base_url}/chat/completions"
        headers = {
            "Authorization": f"Bearer {self.api_key}",
            "Content-Type": "application/json",
        }

        last_err: Exception | None = None
        for attempt in range(max_retries):
            try:
                resp = requests.post(url, headers=headers, json=payload, timeout=self.timeout)
                resp.raise_for_status()
                data = resp.json()
                return self._parse(data)
            except Exception as exc:  # noqa: BLE001 - on retente tout (réseau, 5xx, parse)
                last_err = exc
                time.sleep(min(2 ** attempt, 10))
        raise RuntimeError(f"LLM request failed after {max_retries} tries: {last_err}")

    def _parse(self, data: dict) -> LLMResponse:
        choice = data["choices"][0]
        msg = choice.get("message", {})
        usage_d = data.get("usage", {}) or {}
        usage = LLMUsage(
            prompt_tokens=usage_d.get("prompt_tokens", 0),
            completion_tokens=usage_d.get("completion_tokens", 0),
            total_tokens=usage_d.get("total_tokens", 0),
        )
        self.total_usage.add(usage)

        tool_calls: list[dict] = []
        for tc in msg.get("tool_calls") or []:
            fn = tc.get("function", {})
            args_raw = fn.get("arguments", "{}")
            try:
                args = json.loads(args_raw) if isinstance(args_raw, str) else args_raw
            except json.JSONDecodeError:
                args = {"_raw": args_raw}
            tool_calls.append({"id": tc.get("id", ""), "name": fn.get("name", ""), "arguments": args})

        content = msg.get("content")
        thought = content
        # Fallback : certains modèles (via Ollama) émettent l'appel d'outil en TEXTE JSON
        # dans content au lieu du champ tool_calls natif. On le récupère.
        if not tool_calls and content:
            fb = _fallback_tool_calls(content)
            if fb:
                tool_calls = fb
                thought = _strip_json_blobs(content) or None  # prose restante, pour l'affichage
                content = None  # on évite de dupliquer l'appel dans l'historique

        return LLMResponse(
            content=content,
            tool_calls=tool_calls,
            finish_reason=choice.get("finish_reason", ""),
            usage=usage,
            thought=thought,
            raw=data,
        )

    def ping(self) -> bool:
        """Vérifie que le endpoint répond (utile avant un run)."""
        try:
            r = requests.get(f"{self.base_url}/models", headers={"Authorization": f"Bearer {self.api_key}"}, timeout=10)
            return r.status_code == 200
        except Exception:
            return False


# --- fallback : extraire des appels d'outils depuis du texte JSON --------
import re as _re

_FENCE_RE = _re.compile(r"```(?:json|tool_call)?\s*(\{.*?\}|\[.*?\])\s*```", _re.S)


def _iter_json_blobs(text: str):
    text = text.strip()
    for m in _FENCE_RE.finditer(text):
        yield m.group(1)
    yield text
    # premier objet/liste équilibré dans le texte
    for opn, cls in (("{", "}"), ("[", "]")):
        i = text.find(opn)
        if i != -1:
            depth = 0
            for j in range(i, len(text)):
                if text[j] == opn:
                    depth += 1
                elif text[j] == cls:
                    depth -= 1
                    if depth == 0:
                        yield text[i:j + 1]
                        break


def _normalize_call(obj) -> dict | None:
    if not isinstance(obj, dict):
        return None
    fn = obj.get("function") if isinstance(obj.get("function"), dict) else {}
    name = obj.get("name") or obj.get("tool") or obj.get("tool_name") or fn.get("name")
    if not name or not isinstance(name, str):
        return None
    args = (obj.get("arguments") if obj.get("arguments") is not None else
            obj.get("args") if obj.get("args") is not None else
            obj.get("parameters") if obj.get("parameters") is not None else
            fn.get("arguments", {}))
    if isinstance(args, str):
        try:
            args = json.loads(args)
        except json.JSONDecodeError:
            args = {"_raw": args}
    if not isinstance(args, dict):
        args = {"value": args}
    return {"id": "", "name": name, "arguments": args}


def _fallback_tool_calls(content: str) -> list[dict]:
    for blob in _iter_json_blobs(content):
        try:
            obj = json.loads(blob)
        except (json.JSONDecodeError, TypeError):
            continue
        items = obj if isinstance(obj, list) else [obj]
        calls = [c for c in (_normalize_call(o) for o in items) if c]
        if calls:
            return calls
    return []


def _strip_json_blobs(content: str) -> str:
    """Retire les blocs ```...``` et le premier objet/liste JSON — garde la prose (la 'pensée')."""
    text = _FENCE_RE.sub("", content or "")
    for opn, cls in (("{", "}"), ("[", "]")):
        i = text.find(opn)
        if i != -1:
            depth = 0
            for j in range(i, len(text)):
                if text[j] == opn:
                    depth += 1
                elif text[j] == cls:
                    depth -= 1
                    if depth == 0:
                        text = text[:i] + text[j + 1:]
                        break
    return text.strip()
