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

```mermaid
flowchart LR
    A["Énoncé + fichiers"] --> B["Classification"]
    B --> C["Plan d'action"]
    C --> D["Exécution d'outils"]
    D --> E["Observation"]
    E -->|"Pas de flag"| C
    E -->|"Flag trouvé"| F["Validation + write-up"]
```

## Exemples de cas à résoudre

Dix scénarios typiques de CTF que les agents devront savoir traiter, avec le raisonnement attendu.

### 1. Web : injection SQL sur un formulaire de connexion

```mermaid
flowchart LR
    A["Page de login"] --> B["Tester ' OR 1=1 --"]
    B -->|"Erreur SQL / bypass"| C["Confirmer l'injection"]
    C --> D["UNION SELECT pour lister les tables"]
    D --> E["Extraire la table users / flags"]
    E --> F["Flag"]
```

### 2. Web : jeton JWT mal signé

```mermaid
flowchart LR
    A["Cookie JWT"] --> B["Décoder header + payload"]
    B --> C{"Algorithme ?"}
    C -->|"alg none accepté"| D["Forger un jeton sans signature"]
    C -->|"HS256"| E["Brute-force du secret faible"]
    D --> F["role = admin"]
    E --> F
    F --> G["Accès /admin → Flag"]
```

### 3. Web : inclusion de fichier local (LFI)

```mermaid
flowchart LR
    A["URL ?page=accueil.php"] --> B["Tester ../../../../etc/passwd"]
    B -->|"Contenu affiché"| C["LFI confirmée"]
    C --> D["php://filter base64 sur le code source"]
    D --> E["Trouver le chemin du flag"]
    E --> F["Lire flag.txt → Flag"]
```

### 4. Crypto : chaîne d'encodages

```mermaid
flowchart LR
    A["Texte illisible"] --> B["Détecter l'encodage"]
    B --> C["Base64"]
    C --> D["Hex"]
    D --> E["ROT13 / César"]
    E -->|"Format CTF reconnu"| F["Flag"]
    E -->|"Encore illisible"| B
```

### 5. Crypto : RSA avec paramètres faibles

```mermaid
flowchart LR
    A["n, e, c fournis"] --> B{"Faiblesse ?"}
    B -->|"e = 3, m petit"| C["Racine cubique de c"]
    B -->|"n petit / connu"| D["Factoriser n (factordb, Sage)"]
    B -->|"Facteurs proches"| E["Méthode de Fermat"]
    D --> F["Calculer d puis m = c^d mod n"]
    E --> F
    C --> G["Flag"]
    F --> G
```

### 6. Reverse : crackme vérifiant un mot de passe

```mermaid
flowchart LR
    A["Binaire ELF"] --> B["file + strings"]
    B -->|"Flag en clair"| G["Flag"]
    B -->|"Rien"| C["ltrace / strace : strcmp ?"]
    C -->|"Mot de passe visible"| G
    C -->|"Logique obfusquée"| D["Décompiler (Ghidra)"]
    D --> E["Inverser l'algorithme ou angr"]
    E --> G
```

### 7. Pwn : débordement de tampon (ret2win)

```mermaid
flowchart LR
    A["Binaire + service nc"] --> B["checksec : protections"]
    B --> C["Repérer gets / strcpy"]
    C --> D["Trouver l'offset (pattern cyclique)"]
    D --> E["Adresse de win()"]
    E --> F["Payload pwntools en local"]
    F --> G["Exploit sur le serveur → Flag"]
```

### 8. Forensics : capture réseau (PCAP)

```mermaid
flowchart LR
    A["Fichier .pcap"] --> B["Statistiques des protocoles"]
    B --> C{"Trafic intéressant ?"}
    C -->|"HTTP / FTP"| D["Suivre les flux, extraire les fichiers"]
    C -->|"DNS"| E["Données exfiltrées dans les sous-domaines"]
    C -->|"Identifiants"| F["Mots de passe en clair"]
    D --> G["Flag"]
    E --> G
    F --> G
```

### 9. Stéganographie : image suspecte

```mermaid
flowchart LR
    A["Image PNG / JPG"] --> B["exiftool : métadonnées"]
    B --> C["binwalk : fichiers cachés"]
    C --> D["zsteg / steghide : bits de poids faible"]
    D --> E["Analyse des plans de couleur"]
    B --> F["Flag"]
    C --> F
    D --> F
    E --> F
```

### 10. Misc : service à automatiser

```mermaid
flowchart LR
    A["nc host port"] --> B["Lire les questions"]
    B --> C["Ex. : 100 calculs en 30 s"]
    C --> D["Script pwntools : lire, calculer, répondre"]
    D -->|"Question suivante"| D
    D -->|"Dernière réponse"| E["Flag"]
```

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
