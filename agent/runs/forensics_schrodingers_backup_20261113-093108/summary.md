

---
## Résumé au tour 10 (09:33:01)

## Fait
- Extraction complète de `evidence.zip` et identification des fichiers (SQLite, WAL, JSON, Python).
- Compréhension du mécanisme de sécurité : token = `north XOR south`, clé dérivée de l'historique des tokens.
- Extraction de 474 blobs potentiels de 32 octets depuis le fichier `catalog.db-wal` via l'outil `extract_wal_blobs`.

## Échecs / impasses
- Navigation initiale laborieuse pour localiser `evidence.zip` (chemins imbriqués inattendus).
- Analyse manuelle du WAL avec `xxd` trop fastidieuse pour isoler les données brutes.
- Les 474 blobs extraits sont bruts : il faut encore valider lesquels correspondent aux parts `north` et `south`.

## État actuel
- `capsule.json` est prêt pour le décryptage (ciphertext + nonce AES-GCM).
- `catalog.db-wal` contient les traces des transactions non encore triées.
- On dispose d'une liste de 474 séquences hexadécimales de 32 octets.
- La logique de reconstruction de la clé est comprise, mais pas encore implémentée.

## Prochaines pistes
- Filtrer les 474 blobs pour identifier les paires valides `north` et `south`.
- Reconstituer la séquence chronologique des tokens (XOR des paires).
- Dérivation de la clé de chiffrement à partir de cette séquence.
- Tentative de décryptage de `capsule.json` pour obtenir le flag.


---
## Résumé au tour 20 (09:36:29)

## Fait
- **Analyse cryptographique** : Compréhension du mécanisme dans `recorder.py` (AES-GCM, clé dérivée via SHA256, token = `north XOR south`).
- **Analyse WAL** : Identification du format SQLite WAL (Magic `0x377f0682`, page size 1024, 39 frames).
- **Schéma DB** : Tables `north` et `south` identifiées via `.schema`, contenant les shares BLOB.
- **Extraction brute** : Payloads hexadécimaux détectés dans les frames du WAL (ex: `effa5069...`).

## Échecs / impasses
- **Crash d'exécution** : Le script Python de parsing a planté (`FileNotFoundError`) sur `catalog.db-wal`, probablement un problème de chemin ou de contexte.
- **Incohérence de taille** : Les payloads extraits font 31 octets au lieu des 32 attendus pour les shares (décalage à expliquer).
- **Encodage SQLite** : Lecture directe des BLOBs via `sqlite3` a échoué (problème de décodage UTF-8 sur les données binaires).

## État actuel
- **Cible** : `capsule.json` contient le ciphertext et le nonce, prêt à être déchiffré.
- **Source de vérité** : Le WAL contient l'historique des transactions commitées (`commit_flag=5`).
- **Données** : On a des fragments de données dans les frames, mais pas encore la séquence complète des paires `north`/`south`.
- **Blocage** : Le script d'extraction doit être corrigé pour relire le fichier WAL.

## Prochaines pistes
- **Corriger le script** : Relancer l'analyse du WAL avec le bon chemin absolu.
- **Investiguer le décalage** : Comprendre pourquoi les payloads font 31 octets (encodage SQLite, varint, ou header de cellule).
- **Reconstruction** : Extraire toutes les entrées validées du WAL, reconstruire la séquence de tokens.
- **Déchiffrement** : Dériver la clé finale et tenter de déchiffrer `capsule.json`.


---
## Résumé au tour 30 (09:39:46)

## Fait (actions utiles et ce qu'elles ont donné)
- **Extraction du WAL** : Identification que `catalog.db-wal` manquait dans le dossier racine et extraction réussie depuis `evidence.zip`.
- **Analyse binaire** : Vérification des headers (`SQLite format 3` et `CSAW` dans le WAL), confirmant la validité des fichiers.
- **Compréhension crypto** : Lecture de `OPERATIONS.md` et analyse des snippets, révélant le schéma : `token = north XOR south`, clé = `SHA256(DOMAIN + tokens)`, chiffrement AES-GCM.
- **Initialisation du parser** : Création d'un premier outil `wal_parser` pour extraire les données transactionnelles.

## Échecs / impasses (ce qui n'a PAS marché — à ne pas refaire)
- **Hypothèse de fichier** : Avoir cherché le WAL dans le dossier courant avant de vérifier l'archive `evidence.zip`.
- **Syntaxe Python** : Erreur d'indentation/parenthèse (`unmatched ')'`) dans le script `wal_parser` initial.
- **Gestion des outils** : Tentative d'édition directe d'un outil existant qui s'est révélée impossible (`non modifiable`), perdant du temps sur le `edit_tool`.

## État actuel (ce qu'on sait, fichiers/indices clés)
- **Fichiers critiques** : `catalog.db` (base vide/verrouillée), `catalog.db-wal` (source des données), `capsule.json` (cible chiffrée).
- **Logique validée** : Le WAL contient les transactions avec les valeurs `north` et `south` nécessaires pour reconstruire la clé de déchiffrement.
- **Format WAL** : Header valide (version 3007000), structure de frames connue (32 octets header + pages).

## Prochaines pistes
- **Corriger le parser** : Écrire un script Python propre (nouvel outil) pour lire les frames du WAL et extraire les blobs `north`/`south`.
- **Calculer la clé** : Implémenter la fonction de dérivation de clé (XOR des tokens + SHA256).
- **Déchiffrement** : Utiliser la clé dérivée pour déchiffrer `capsule.json` ou les données de la base et récupérer le flag.
