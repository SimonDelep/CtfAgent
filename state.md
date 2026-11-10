# État du projet CtfAgent

Synthèse de ce qui a été construit et de son fonctionnement. Ce document décrit
l'implémentation réelle du dépôt, pas l'intention du `Readme.md`.

> Dernière mise à jour : 2026-11-10

---

## 1. Ce qui a été fait

Implémentation du squelette complet de l'architecture **Dream-RSI** décrite dans
`Readme.md`, suivant exactement son arborescence, plus une extension :
**la capacité pour l'agent de forger ses propres outils** (dite « option 2 »).

Principe fondateur conservé : **les poids du modèle ne changent jamais**. Ce qui
évolue, c'est la *stratégie* (`policy/vN/`, du texte) et, désormais, les *outils
forgés* (`policy/vN/tools/`, du code Python validé puis adopté).

État par composant :

| Composant | Fichier | État |
|---|---|---|
| ① Chargeur anti-triche | `core/loader.py` | **complet** |
| ② Client LLM (Ollama/vLLM) | `core/llm.py` | **complet** |
| ③ Sandbox Docker | `core/sandbox.py` | squelette + garde-fou ; `_run_in_container` à finaliser selon l'infra |
| ③ Définition des tools | `core/tools.py` | **complet** (jeu de base + `create_tool`) |
| ④ Stratégie de départ | `policy/v0/` | **complet** (générique) |
| ⑤ Boucle d'agent | `core/agent.py` | **complet** (réel = rêve) |
| ⑥ Arbre de recherche | `core/tree.py` | **complet** (SQLite) |
| ⑦ Simulateur | `dream/simulator.py` | **complet** |
| ⑧ Rêveur + juge | `dream/dreamer.py` | fonctionnel ; juge déterministe (juge LLM branchable) |
| ⑨ Réflecteur | `dream/reflector.py` | **complet** (éditions + filtre anti-fuite) |
| ⑩ Porte de validation | `runner/gate.py` | **complet** |
| Orchestrateur (boucle RSI) | `runner/rsi_loop.py` | **complet** |
| Évaluation finale | `runner/evaluate.py` | **complet** |
| **Forgeron d'outils (option 2)** | `core/forge.py` | **complet** |

Types partagés et interfaces : `core/types.py`.

Points laissés aux coéquipiers (interfaces prêtes, marquées TODO) :
- `core/sandbox.py::_run_in_container` — exécution Docker réelle.
- `core/sandbox.py` tool `remote` — branchement pwntools/curl vers le service.
- `dream/dreamer.py` — juge LLM plus fin (via `judge_fn`).
- `dream/reflector.py` — génération d'éditions par LLM (repli déterministe en place).

---

## 2. Arborescence

```
CtfAgent/
├── core/
│   ├── llm.py            ② client LLM (API compatible OpenAI, sans dépendance)
│   ├── loader.py         ① chargeur anti-triche
│   ├── sandbox.py        ③ exécution Docker (garde-fou enabled=False)
│   ├── tools.py          ③ définition des tools + create_tool
│   ├── forge.py          ⑪ forgeron d'outils (option 2)
│   ├── agent.py          ⑤ boucle d'agent (identique réel/rêve)
│   ├── tree.py           ⑥ arbre de recherche (SQLite)
│   └── types.py          types partagés + interfaces (Protocol World…)
├── dream/
│   ├── simulator.py      ⑦ simulateur (rejoue l'arbre ; [NON SIMULÉ] sinon)
│   ├── dreamer.py        ⑧ rêveur + juge
│   └── reflector.py      ⑨ réflecteur (≤3 éditions + filtre anti-fuite)
├── policy/
│   └── v0/               ④ stratégie de départ (générique)
│       ├── prompt.md
│       ├── heuristics.md
│       ├── skills/        recon.md, flag_format.md
│       └── tools/         outils forgés adoptés (vide au départ)
├── runner/
│   ├── gate.py           ⑩ porte de validation
│   ├── rsi_loop.py       ⟵ ORCHESTRATEUR (boucle principale) + CLI
│   └── evaluate.py       évaluation (seul composant à lire le vrai flag)
├── data/                 trees.db + forge/live (créés à l'exécution ; gitignoré)
├── CSAW26_LLMAC_DB/      base de challenges (sous-module, à initialiser)
├── .env.example          config LLM
├── requirements.txt
└── state.md              ce document
```

---

## 3. Fonctionnement de la boucle RSI (l'orchestrateur)

`runner/rsi_loop.py` → classe `RSIOrchestrator`. Elle enchaîne les 5 étapes du
README :

```
1. RÉEL       L'agent ⑤ attaque les challenges d'entraînement dans la sandbox ③.
              Chaque action (hypothèse → tool → observation) crée un nœud dans
              l'arbre ⑥. Le chemin menant au flag est marqué.

2. RÊVE       Sur les tentatives résolues, on repère les « mauvaises
              bifurcations » (un bon état d'où l'agent est parti dans une
              mauvaise direction) et le rêveur ⑧ les rejoue via le simulateur ⑦,
              hors ligne. Le juge note chaque branche. Un flag rêvé ne compte
              jamais.

3. RÉFLEXION  Le réflecteur ⑨ transforme les rêves en ≤3 modifications de
              stratégie (heuristiques / skills), chacune justifiée, filtrées
              contre toute fuite (nom de challenge, flag). On ajoute aussi les
              outils forgés utiles (option 2) à la candidate v(n+1).

4. VALIDATION La porte ⑩ évalue baseline vs candidate sur l'ensemble de
              VALIDATION. Adoption seulement si : au moins autant de flags, et à
              nombre égal, strictement moins d'étapes. Sinon la candidate est
              effacée.

5. FINAL      Après N itérations, évaluation unique sur l'ensemble de TEST
              (CSAW 2026), jamais utilisé pour rêver.
```

Garde-fou : tant que `enable_sandbox=False` (défaut), **aucune commande Docker
n'est exécutée**. L'orchestrateur est pilotable « à sec » pour vérifier le
câblage sans rien lancer.

### Séparation des données (anti-fuite)
- **train / val / test** sont disjoints. Le test (CSAW 2026) ne sert jamais à
  rêver ni à valider.
- Le chargeur ① ne copie dans le workspace que l'énoncé et les fichiers listés :
  jamais `solution/`, `solve.py`, `writeup.md`, ni le flag.
- Le flag attendu n'est lu que par `runner/evaluate.py`, pour le score.
- Le réflecteur ⑨ retire des stratégies tout flag (`...{...}`) et tout nom de
  challenge connu.

---

## 4. L'agent et les outils

### Boucle d'agent (`core/agent.py`)
Le LLM répond par un JSON strict `{"hypothesis", "tool", "args"}`. La boucle :
- `set_hypothesis` → ouvre une nouvelle branche de l'arbre ;
- `submit_flag` → valide le FORMAT et clôt si bon ;
- un tool concret → exécuté par le `World` (sandbox en réel, simulateur en rêve) ;
- un flag repéré dans une sortie → clôt aussi la tentative.

Le **même code** tourne en réel et en rêve : seule l'implémentation de `World`
change (interface dans `core/types.py`).

### Tools de base (`core/tools.py`)
`run_cmd`, `python_exec`, `read_file`, `remote`, et les méta `set_hypothesis`,
`submit_flag`, `create_tool`.

---

## 5. Option 2 — l'agent forge ses propres outils

Quand l'agent bloque, il peut fabriquer un outil réutilisable. C'est le rôle du
**forgeron** `core/forge.py` (`ToolForge`).

### Déroulé
1. L'agent appelle `create_tool(name, description, args, code)`, où `code`
   définit `def run(args: dict) -> str:`.
2. Le forgeron **valide** (voir ci-dessous), **emballe** le code dans un script
   autonome (en-tête de métadonnées + `run()` + harnais `__main__`), l'écrit
   dans `data/forge/live/<name>.py` et l'**enregistre** : l'outil est utilisable
   immédiatement, comme un tool normal.
3. À l'exécution, l'outil tourne **dans la sandbox** :
   `python3 -I /forge/<name>.py '<json args>'`, `--network none`, magasin monté
   en lecture seule.
4. En fin de phase réelle, les outils **utilisés sur un chemin gagnant** sont
   promus par l'orchestrateur dans la candidate `policy/v(n+1)/tools/`.
5. La porte ⑩ valide la candidate (outils compris) : adoptée seulement si elle
   fait mieux. Sinon les outils sont rejetés avec elle.

Ainsi un outil forgé suit exactement le même cycle apprentissage → validation →
adoption que la stratégie, et persiste **versionné**.

### Sécurité
- Le code est écrit par le LLM : il n'est **jamais exécuté sur l'hôte**, seulement
  dans le conteneur isolé, sans réseau, en lecture seule.
- **Validation statique** avant écriture : syntaxe valide (AST), présence de
  `def run(args)`, nom conforme `[a-z][a-z0-9_]…` ne réutilisant pas un tool de
  base, et rejet de motifs destructeurs (`rm -rf /`, `shutil.rmtree('/')`, fork
  bomb, `mkfs`, `/etc/shadow`, `os.fork`).
- `enable_sandbox=False` par défaut : rien ne s'exécute réellement tant qu'on ne
  l'active pas.

> Note : cette capacité n'est pas décrite dans `Readme.md`, qui limite
> l'évolution au texte. C'est une extension assumée.

---

## 6. Comment lancer (rappel)

Configuration LLM via `.env` (modèle par défaut : `huihui_ai/qwen3.5-abliterated:122b`
sur Ollama, `http://127.0.0.1:11434/v1`).

```bash
# À sec : découpe des données + câblage, sans rien exécuter
python -m runner.rsi_loop --dry-run

# Boucle RSI sans LLM (triage/câblage), sans Docker
python -m runner.rsi_loop --no-llm --iterations 2

# Boucle réelle (active Docker ET le LLM) — à faire tourner sciemment
python -m runner.rsi_loop --enable-sandbox --iterations 3
```

Prérequis pour une vraie exécution :
- initialiser le sous-module `CSAW26_LLMAC_DB` (actuellement vide) ;
- construire l'image Docker de la sandbox et finaliser `_run_in_container` ;
- un serveur LLM accessible (Ollama sur le DGX).

---

## 7. État de validation

Vérifié **hors ligne** (sans modèle, sans Docker) :
- tous les modules compilent et s'importent ;
- orchestrateur exécuté de bout en bout sur une base synthétique (découpe
  train/val/test, phase réelle, rêve, réflexion, validation, éval finale) ;
- arbre → détection des mauvaises bifurcations → jugement correct (une
  bifurcation ne « rejoint » pas le chemin par le seul fait que son parent y est) ;
- filtre anti-fuite : flag et nom de challenge retirés d'une stratégie ;
- porte : +flag adopté, −étapes adopté, −flag rejeté ;
- forge : validation (accept/refus), harnais exécutable en `-I`, rechargement
  d'un outil depuis une version, promotion d'un outil utilisé sur un chemin
  gagnant.

Non exécuté (volontairement) : aucune commande Docker, aucun appel au modèle,
aucun commit.
