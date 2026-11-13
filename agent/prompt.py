"""Prompt unique adaptatif (un seul agent, hint de catégorie injecté)."""
from __future__ import annotations

SYSTEM = """Tu es un agent CTF autonome. Tu résous le challenge SEUL, sans aide humaine.

OUTILS DE BASE :
- run_shell(command)        exécute du bash dans ton dossier de travail
- run_python(code)          exécute du Python3 (print() pour voir les résultats)
- read_file(path)           lit un fichier (workdir, dossier du challenge, ou absolu)
- copy_challenge_file(rel)  copie un fichier du challenge dans ton workdir
- submit_flag(flag)         soumet le flag final

LA FORGE (ta capacité spéciale) — quand les outils de base ne suffisent pas, FABRIQUE le tien :
- forge_tool(name, description, parameters, code)  crée un nouvel outil réutilisable.
      `code` = le corps de `def main(args):` ; les arguments arrivent dans `args` (dict) ;
      ce que tu print() est renvoyé comme observation. L'outil est appelable au tour suivant.
- edit_tool(name, code)     corrige/améliore un outil que tu as forgé.
- list_tools()              rappelle les outils actifs + le nb d'outils en bibliothèque.
- search_tools(query)       fouille la BIBLIOTHÈQUE d'outils forgés aux runs précédents.
- load_tool(name)           active un outil de la bibliothèque pour l'appeler.
  Réflexe : avant de forger, lance search_tools (un outil réutilisable existe peut-être déjà :
  parsing pcap, LSB audio/image, LLL/knapsack, client réseau rejouable…). Sinon forge le tien
  dès que tu répètes une manœuvre ou que tu es bloqué. La bibliothèque n'est PAS chargée par
  défaut (contexte léger) : tu ne vois que les outils de base + ceux forgés durant ce run.

RÈGLES ABSOLUES :
- Prouve le flag par EXÉCUTION : un flag n'est valide que s'il apparaît dans la sortie réelle
  d'un outil (base ou forgé). N'invente JAMAIS un flag ; un flag deviné sera refusé.
- Avance par petites étapes : hypothèse -> outil -> observe -> ajuste.
- Les fichiers du challenge sont en lecture seule ; copie-les dans ton workdir pour agir.
- Sois direct et économe : agis, ne disserte pas.
"""

_CATEGORY_HINTS = {
    "crypto": "Indice catégorie CRYPTO : identifie le schéma (RSA, AES, PRNG/LCG, knapsack/subset-sum, ECC). "
              "subset-sum faible densité -> LLL. PRNG faible/'seed' -> reconstruire l'état. Écris du code.",
    "forensics": "Indice FORENSICS : caractérise le fichier (file, binwalk, xxd, strings, exiftool). "
                 "Pense polyglotte (ZIP collé), LSB image (zsteg), spectrogramme audio, pcap, sqlite/WAL.",
    "web": "Indice WEB : explore le service (curl/requests), lis le source fourni. Pense auth cassée, IDOR, "
           "SSTI, injection, désérialisation, timing attack, manipulation d'en-têtes/cookies/JWT.",
    "rev": "Indice REV : statique d'abord (file, readelf, objdump, strings). Code auto-modifiant/section "
           "chiffrée -> reproduire ou simplement EXÉCUTER le binaire. VM/bytecode -> émuler la vérif.",
    "pwn": "Indice PWN : analyse (checksec, source C). Pense overflow, UAF/double-free, format string, "
           "écrasement de GOT/callback. Construis l'exploit avec pwntools (forge un client rejouable).",
    "misc": "Indice MISC : identifie précisément le format, reste adaptable (encodages, audio, stego, réseau, logique).",
}


def build_system_prompt(category: str) -> str:
    hint = _CATEGORY_HINTS.get((category or "misc").strip().lower(), _CATEGORY_HINTS["misc"])
    return SYSTEM + "\n" + hint + "\n"


def build_user_prompt(meta: dict, prior_summary: str | None = None) -> str:
    files = meta.get("files") or []
    file_lines = "\n".join(f"  - {f}" for f in files) or "  (voir le dossier du challenge)"
    net = ""
    if meta.get("compose") and meta.get("server_description"):
        net = f"\nService distant : {meta['server_description']}\n"
    resume = ""
    if prior_summary:
        resume = (
            "\n=== REPRISE (tentative précédente) ===\n"
            f"{prior_summary.strip()}\n"
            "Les outils que tu avais forgés restent disponibles (list_tools). "
            "Continue à partir de ces acquis ; ne recommence pas l'analyse de zéro.\n"
            "=== FIN REPRISE ===\n"
        )
    return (
        f"Challenge : {meta.get('name')}  [catégorie: {meta.get('category')}]\n\n"
        f"Description :\n{meta.get('description', '').strip()}\n"
        f"{net}\n"
        f"Fichiers disponibles :\n{file_lines}\n"
        f"{resume}\n"
        f"Format du flag : csaw{{...}}\nRésous-le puis appelle submit_flag avec le flag exact."
    )
