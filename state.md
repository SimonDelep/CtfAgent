# État du projet CtfAgent — branche `weight`

Synthèse de l'implémentation sur la branche `weight`. Elle **inverse l'invariant
du README** : au lieu de faire évoluer la *stratégie* en prenant le meilleur du
rêve, on fait évoluer les **poids** du modèle. La stratégie `policy/v0` reste
figée.

> Branche dérivée de `dreamer`. Dernière mise à jour : 2026-11-10

---

## 1. Ce qui change par rapport à `dreamer`

| Aspect | `dreamer` | `weight` (cette branche) |
|---|---|---|
| Ce qui évolue | la stratégie (`policy/vN/`, texte) | les **poids** (`weights/vN/`, LoRA) |
| Issue du rêve | éditions de stratégie (réflecteur ⑨) | **jeu d'entraînement** (entraîneur) |
| Adoption | nouvelle stratégie si meilleure | nouvelle **version de poids** si meilleure |
| Composant clé | `dream/reflector.py` | `core/trainer.py` |
| Stratégie | évolue | **figée** à `policy/v0` |

`dream/reflector.py` a été retiré ; `core/trainer.py` le remplace. Tout le reste
(chargeur, client LLM, sandbox, tools, forge, boucle d'agent, arbre, simulateur,
rêveur, porte, évaluation) est inchangé.

---

## 2. Arborescence (delta)

```
CtfAgent/
├── core/
│   ├── trainer.py        ⟵ NOUVEAU : entraîneur de poids (remplace reflector)
│   ├── llm.py            + helper with_model() pour servir une version de poids
│   ├── types.py          + WeightVersion, TrainingExample
│   └── … (agent, forge, sandbox, tools, tree, loader inchangés)
├── dream/
│   ├── simulator.py, dreamer.py   (inchangés ; reflector.py SUPPRIMÉ)
├── weights/
│   └── v0/manifest.json  ⟵ NOUVEAU : modèle de base gelé (point de départ)
├── policy/v0/            stratégie FIGÉE (ne change plus)
├── runner/
│   ├── rsi_loop.py       ⟵ RÉÉCRIT : WeightRSIOrchestrator
│   ├── gate.py, evaluate.py   (inchangés : la porte compare des EvalResult)
└── …
```

Les versions de poids apprises (`weights/v1/`, `v2/`, …) sont gitignorées ; seule
`weights/v0` (manifeste de base) est versionnée.

---

## 3. La boucle (évolution des poids)

```
1. RÉEL        L'agent ⑤ attaque le train avec la version de poids courante
               (le client LLM sert `weights.model_ref`). Arbres enregistrés ⑥.

2. RÊVE        Le rêveur ⑧ rejoue les mauvaises bifurcations via le simulateur ⑦.

3. ENTRAÎNEMENT  L'entraîneur (core/trainer.py) :
               - construit un JEU D'ENTRAÎNEMENT par rejection sampling :
                 uniquement les trajectoires VÉRIFIÉES gagnantes (chemin menant
                 au vrai flag) + les meilleurs rêves qui rejoignent ce chemin,
                 pondérés par leur score ;
               - produit une version de poids candidate v(n+1) (LoRA, base gelée).

4. VALIDATION  La porte ⑩ compare la version courante et la candidate sur
               l'ensemble de VALIDATION. Adoption seulement si au moins autant de
               flags, et à nombre égal, strictement moins d'étapes.

5. FINAL       Évaluation unique sur le TEST (CSAW 2026), jamais vu.
```

Servir une version de poids = pointer le client LLM vers son `model_ref`
(`LLMClient.with_model`). Une version = un manifeste `weights/vN/manifest.json`
(`base_ref` gelé, `model_ref` servi, `adapter_path` LoRA) + `dataset.jsonl`
(traçabilité du jeu d'entraînement).

---

## 4. Garde-fous (importants)

Cette inversion introduit des risques réels (voir la discussion en annexe) ;
les garde-fous en place :

- **Rejection sampling strict** : on n'entraîne que sur des trajectoires
  vérifiées gagnantes et des rêves qui rejoignent le chemin. Jamais un flag rêvé,
  jamais une étape perdante. Limite la mémorisation de solutions fausses.
- **Base gelée + LoRA** : `base_ref` ne change jamais ; une version = base +
  adaptateur. C'est réversible, auditable, versionné.
- **Porte sur held-out** : une version n'est adoptée que si elle fait mieux sur
  l'ensemble de validation, disjoint du test.
- **Entraînement désactivé par défaut** (`enable_training=False`). Le fine-tuning
  réel dépend d'une infra absente ici ; sans elle, l'entraîneur renvoie une
  candidate identique à la base (non adoptée). Point d'extension :
  `core/trainer.py::_run_finetune`.
- **Sandbox désactivée par défaut** (`enable_sandbox=False`) : aucun Docker.

Risques non entièrement couverts, à garder en tête : contamination (une solution
peut s'imprimer dans les poids — ne jamais entraîner sur val/test), oubli
catastrophique sur peu d'exemples, surajustement de la sélection si trop de
candidates sur un petit held-out, coût (fine-tuning d'un 122B hors de portée du
DGX Spark en l'état).

---

## 5. Lancer

```bash
# À sec : découpe + câblage, sans rien exécuter
python -m runner.rsi_loop --dry-run

# Boucle sans LLM ni entraînement (vérifie le câblage)
python -m runner.rsi_loop --no-llm --iterations 2

# Boucle réelle : nécessite Docker, un LLM, ET une infra de fine-tuning
python -m runner.rsi_loop --enable-sandbox --enable-training --iterations 3
```

Prérequis pour une vraie exécution :
- initialiser le sous-module `CSAW26_LLMAC_DB` (actuellement vide) ;
- image Docker de la sandbox + `_run_in_container` finalisé ;
- un serveur LLM (Ollama/vLLM) ;
- **une chaîne de fine-tuning LoRA** branchée dans `_run_finetune`, servant le
  résultat sous un `model_ref` dédié (p. ex. créer un modèle Ollama via Modelfile,
  ou charger l'adaptateur côté vLLM).

---

## 6. État de validation

Vérifié **hors ligne** (sans modèle, sans Docker, sans entraînement) :
- compilation de tous les modules ;
- boucle poids exécutée de bout en bout à sec (v0 → entraînement désactivé →
  candidate identique à la base → arrêt propre → éval finale) ;
- `build_examples` : extraction d'exemples (contexte → action) depuis un chemin
  gagnant (source `real-solution`) ;
- `train` à sec : candidate `is_base`, `dataset.jsonl` écrit pour audit ;
- garde-fou : `enable_training=True` sans infra lève `NotImplementedError`.

Non exécuté (volontairement) : aucun Docker, aucun appel modèle, aucun
fine-tuning.

---

## Annexe — pourquoi c'est risqué (rappel)

Faire évoluer les poids répond à une AUTRE question que le README (« le texte
seul suffit-il ? »). Mélangé naïvement, cela empêche d'attribuer un gain à la
stratégie ou aux poids. L'approche retenue ici — bras séparé, base gelée +
LoRA versionné, porte sur held-out, rejection sampling — permet de mesurer la
valeur marginale des poids tout en limitant contamination et surapprentissage.
Pour une comparaison honnête, évaluer `dreamer` (texte seul) vs `weight`
(texte figé + poids) sur le même split.
