# CtfAgent

Projet réalisé dans le cadre du semestre 3 à l'UQAC.

## Objectif

CtfAgent vise à concevoir des **agents autonomes basés sur des LLM capables de résoudre des défis CTF (Capture The Flag)** de bout en bout : analyser l'énoncé, explorer les fichiers ou services fournis, exécuter des outils, raisonner sur les résultats et retrouver le flag, sans intervention humaine.

L'objectif est d'évaluer jusqu'où un agent peut aller seul sur des challenges de sécurité, et quelles architectures (agent unique, multi-agents, agents spécialisés par catégorie) donnent les meilleurs résultats.

## Périmètre

Catégories de challenges visées :

- **Web** : injections, failles d'authentification, mauvaises configurations
- **Crypto** : chiffrements faibles, mauvaises utilisations de primitives
- **Reverse** : analyse de binaires et de scripts
- **Pwn** : exploitation de binaires (débordements, format strings…)
- **Forensics / Stéganographie** : analyse de fichiers, captures réseau, images
- **Misc** : encodages, scripting, énigmes

## Fonctionnement envisagé

1. **Lecture du challenge** : l'agent reçoit l'énoncé, les fichiers joints et/ou l'adresse du service.
2. **Classification** : identification de la catégorie et choix de la stratégie (ou d'un agent spécialisé).
3. **Boucle d'action** : l'agent planifie, exécute des commandes et des outils (`file`, `strings`, `binwalk`, `nmap`, `curl`, Python, `pwntools`, Ghidra…), observe les résultats et ajuste son approche.
4. **Validation** : détection du format de flag (ex. `CTF{...}`) et vérification de la réponse.
5. **Rapport** : production d'un write-up retraçant la démarche suivie.

## Sécurité et éthique

- Les agents s'exécutent dans un **environnement isolé** (conteneur / VM) : ils ne doivent pas affecter la machine hôte.
- Ils ne ciblent que des **challenges CTF autorisés** (plateformes d'entraînement, CTF locaux ou compétitions dont les règles permettent l'usage d'outils automatisés).
- Aucune clé API ni aucun secret ne doit être commité : utiliser un fichier `.env` (ignoré par git).

## Structure du dépôt

> À compléter au fur et à mesure du développement.

```
CtfAgent/
├── Readme.md
└── ...
```

## Installation

> À compléter (dépendances, configuration des clés API, lancement de l'environnement isolé).

## Utilisation

> À compléter.

## Équipe

- Simon
- …
