"""Client LLM unique de CtfAgent.

Point d'accès à tout modèle exposant l'API compatible OpenAI (Ollama sur le
DGX, vLLM, etc.). Volontairement sans dépendance : utilise `urllib`, donc rien
à installer. Aucune requête n'est émise à l'import.

Configuration par variables d'environnement (voir `.env.example`) :
  - CTFAGENT_LLM_BASE_URL  (déf. http://127.0.0.1:11434/v1  → Ollama)
  - CTFAGENT_LLM_MODEL     (déf. huihui_ai/qwen3.5-abliterated:122b)
  - CTFAGENT_LLM_API_KEY   (déf. "ollama" ; ignoré par Ollama)
  - CTFAGENT_LLM_TIMEOUT   (déf. 600 secondes)
"""
from __future__ import annotations

import json
import os
import re
import urllib.error
import urllib.request
from dataclasses import dataclass
from typing import Any


class LLMError(RuntimeError):
    """Erreur de communication avec le serveur de modèle."""


@dataclass
class LLMConfig:
    base_url: str = "http://127.0.0.1:11434/v1"
    model: str = "huihui_ai/qwen3.5-abliterated:122b"
    api_key: str = "ollama"
    timeout: float = 600.0
    temperature: float = 0.2

    @classmethod
    def from_env(cls) -> "LLMConfig":
        return cls(
            base_url=os.environ.get("CTFAGENT_LLM_BASE_URL", cls.base_url).rstrip("/"),
            model=os.environ.get("CTFAGENT_LLM_MODEL", cls.model),
            api_key=os.environ.get("CTFAGENT_LLM_API_KEY", cls.api_key),
            timeout=float(os.environ.get("CTFAGENT_LLM_TIMEOUT", cls.timeout)),
            temperature=float(os.environ.get("CTFAGENT_LLM_TEMPERATURE", cls.temperature)),
        )


class LLMClient:
    """Client minimal `chat/completions`.

    Sert les quatre rôles du README (acteur, juge, réflecteur, modèle du monde)
    via le même point d'accès ; le rôle est porté par les messages, pas par le
    client.
    """

    def __init__(self, config: LLMConfig | None = None) -> None:
        self.config = config or LLMConfig.from_env()

    def with_model(self, model: str) -> "LLMClient":
        """Renvoie un client identique pointant vers un autre modèle servi.

        Sert à la branche weight : évaluer une version de poids = servir un
        `model_ref` différent (base, ou base+adaptateur fusionné) sur le même
        backend, sans changer le reste de la configuration.
        """
        import dataclasses

        return LLMClient(dataclasses.replace(self.config, model=model))

    def chat(
        self,
        messages: list[dict[str, str]],
        *,
        temperature: float | None = None,
        max_tokens: int = 1024,
        stop: list[str] | None = None,
        extra: dict[str, Any] | None = None,
    ) -> str:
        """Envoie une conversation et renvoie le texte de la réponse."""
        payload: dict[str, Any] = {
            "model": self.config.model,
            "messages": messages,
            "temperature": self.config.temperature if temperature is None else temperature,
            "max_tokens": max_tokens,
        }
        if stop:
            payload["stop"] = stop
        if extra:
            payload.update(extra)

        url = f"{self.config.base_url}/chat/completions"
        body = json.dumps(payload).encode()
        req = urllib.request.Request(
            url,
            data=body,
            headers={
                "Content-Type": "application/json",
                "Authorization": f"Bearer {self.config.api_key}",
            },
            method="POST",
        )
        try:
            with urllib.request.urlopen(req, timeout=self.config.timeout) as resp:
                data = json.load(resp)
        except urllib.error.URLError as exc:  # réseau, serveur éteint…
            raise LLMError(f"Appel LLM échoué ({url}) : {exc}") from exc
        except (json.JSONDecodeError, KeyError) as exc:
            raise LLMError(f"Réponse LLM illisible : {exc}") from exc

        try:
            return data["choices"][0]["message"]["content"]
        except (KeyError, IndexError, TypeError) as exc:
            raise LLMError(f"Réponse LLM sans contenu : {data!r}") from exc

    def complete_json(
        self,
        messages: list[dict[str, str]],
        *,
        max_tokens: int = 512,
        temperature: float | None = None,
    ) -> dict[str, Any]:
        """Comme `chat`, mais extrait le premier objet JSON de la réponse.

        Tolère les modèles qui entourent le JSON de texte ou de blocs ```json.
        Lève `LLMError` si aucun objet JSON exploitable n'est trouvé.
        """
        raw = self.chat(messages, temperature=temperature, max_tokens=max_tokens)
        obj = _extract_json_object(raw)
        if obj is None:
            raise LLMError(f"Aucun JSON dans la réponse LLM : {raw[:300]!r}")
        return obj


def _extract_json_object(text: str) -> dict[str, Any] | None:
    """Trouve le premier objet `{...}` valide dans une chaîne."""
    # Bloc ```json ... ``` prioritaire.
    fence = re.search(r"```(?:json)?\s*(\{.*?\})\s*```", text, re.DOTALL)
    candidates = []
    if fence:
        candidates.append(fence.group(1))
    # Puis balayage par équilibrage d'accolades.
    start = text.find("{")
    while start != -1:
        depth = 0
        for i in range(start, len(text)):
            if text[i] == "{":
                depth += 1
            elif text[i] == "}":
                depth -= 1
                if depth == 0:
                    candidates.append(text[start : i + 1])
                    break
        start = text.find("{", start + 1)
        if len(candidates) > 5:
            break
    for cand in candidates:
        try:
            obj = json.loads(cand)
            if isinstance(obj, dict):
                return obj
        except json.JSONDecodeError:
            continue
    return None
