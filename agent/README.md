# Agent CTF autonome — CSAW LLM 2026

Agent maison qui résout des challenges CTF **sans intervention humaine**, piloté par un
modèle **local via Ollama**. Exécution **directe sur l'hôte** (pas de Docker). Produit pour
chaque challenge : un **flag prouvé par exécution**, un **transcript** et un **write-up**.

## Les idées originales
1. **Forge à outils** : quand les outils de base ne suffisent pas (ou que l'agent est bloqué),
   le modèle **crée ou modifie son propre outil** à la volée (`forge_tool`/`edit_tool`). L'outil
   est validé, chargé à chaud, et appelable au tour suivant. Les outils forgés sont **partagés**
   (`forge/lib/`) → l'agent capitalise d'un challenge à l'autre.
2. **Verifier *grounded*** : un flag n'est accepté que s'il apparaît dans une **sortie d'outil
   réelle** (base ou forgé) → zéro flag halluciné.

## Anti-blocage / mémoire / observabilité
- **Détecteur de répétition** : un appel d'outil **identique** répété `repeat_threshold` fois (défaut 3)
  est **court-circuité** (résultat renvoyé depuis le cache + avertissement « change d'approche »).
- **Détecteur de blocage** : après `stuck_threshold` tours sans sortie utile → *nudge* vers la Forge.
- **Résumé périodique + mémoire d'approches** : tous les `summary_interval` tours (défaut 10), le
  modèle écrit un résumé *(Fait / Échecs / État / Pistes)* dans **`summary.md` (un par run de
  challenge)**, qui **remplace l'historique détaillé** (compactage du contexte → pas de dépassement
  de fenêtre, et les impasses ne sont pas répétées).
- **Affichage live** dans le terminal : 🧠 pensée → 🔧 action → ↳ résultat. Désactivable avec
  `--quiet` (ou `ui.stream: false`).

## Architecture
```
orchestrator.py    prépare runs/<chal>/work, câble tout, lance la boucle
  prompt.py          prompt unique adaptatif (hint de catégorie)
  llm_client.py      client OpenAI-compatible (Ollama) + fallback tool-calls en JSON
  core/loop.py       boucle ReAct + détecteur de blocage (→ nudge Forge)
  core/registry.py   registre unifié : outils de base (natifs) + forgés (fichiers)
  core/forge.py      forge_tool / edit_tool / list_tools + validation + hot-reload
  core/executor.py   exécution LOCALE (subprocess, timeout, cwd=work, python3 -I)
  core/verifier.py   validation 'grounded' du flag
  core/report.py     transcript.jsonl + writeup.md
  forge/lib/         outils forgés partagés (réutilisables entre challenges)
  eval/run.py        harness de scoring (métriques agrégées → report.md)
```

### Un outil forgé = un fichier
```python
SCHEMA = { "name": "...", "description": "...", "parameters": {...} }  # ajouté par la Forge
def main(args):          # écrit par le LLM ; print() = observation renvoyée
    ...
# footer standard ajouté par la Forge (lit args JSON en argv, appelle main)
```

## Prérequis
```bash
pip install -r agent/requirements.txt         # requests + pyyaml (côté hôte)
# Outillage CTF utile aux outils forgés (dans l'env Python de l'hôte) :
pip install pwntools pycryptodome sympy z3-solver numpy pillow requests scapy
# + binutils, binwalk, zsteg, sox, sqlite3, gdb selon les challenges.

# Modèle : configuré dans le fichier .env (chargé automatiquement), à la racine du projet :
#   LLM_BASE_URL=http://localhost:11434/v1
#   LLM_API_KEY=ollama
#   LLM_MODEL=huihui_ai/qwen3.5-abliterated:122b
# (copier .env.example -> .env ; une variable exportée dans le shell reste prioritaire)
```

## Utilisation
```bash
python -m agent.orchestrator CSAW-Quals/crypto/secret_treaties   # un challenge
python -m agent.eval.run --pilots                                 # 1 par catégorie
python -m agent.eval.run                                          # tout le benchmark
```
Sorties : `agent/runs/<cat>_<chal>_<ts>/` (transcript.jsonl, writeup.md, result.json,
work/, forge/) + tableau agrégé `agent/eval/report.md`.

## Traçabilité & reprise
- **Logs par run** (`agent/runs/<cat>_<chal>_<ts>/`) : `transcript.jsonl` (1 ligne/événement
  horodatée : prompts, **pensée**, appels d'outils + arguments, résultats, résumés, flag),
  `writeup.md`, `summary.md`, `result.json`.
- **Ledger** (`agent/runs/ledger.json`) : suivi persistant mis à jour après **chaque** run.
  À la reprise, `eval/run.py` **saute les challenges déjà résolus** et **réessaie les échecs**.
  ```bash
  python -m agent.eval.run              # reprend là où on s'était arrêté
  python -m agent.eval.run --force      # relance tout, y compris les résolus
  python -m agent.eval.run --status     # affiche le tableau de suivi
  ```

## Mode compétition (flag inconnu)
```bash
python -m agent.orchestrator <chal> --no-ground-truth
```
Le verifier accepte alors le 1er flag bien formé **issu d'une sortie d'outil**.

## Notes
- **Tool-calling Ollama** : certains modèles renvoient l'appel en texte JSON plutôt que dans
  `tool_calls`. `llm_client.py` récupère ces deux formes automatiquement.
- **Containment** : l'exécution est locale (demande de l'utilisateur). Pour durcir plus tard,
  envelopper `executor._run` dans `timeout`/`firejail`/`bwrap`.
- **Validé** : boucle + forge + verifier testés hors-ligne (exécution réelle) et en live sur
  Ollama (le 7b a spontanément forgé puis édité un outil face à un WAV).
