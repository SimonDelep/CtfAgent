

---
## Résumé au tour 10 (02:14:32)

## Fait
- Localisé et extrait `evidence.zip` (les fichiers étaient absents du dossier de travail initial).
- Identifié les composants : base SQLite (`catalog.db` + `.wal`), payload chiffré (`capsule.json`), logique de dérivation (`recorder.py`).
- Compris le mécanisme de chiffrement : `token = north XOR south` (32 octets), utilisé comme clé AES-GCM.

## Échecs / impasses
- Perte de temps initiale avec `ls` dans un dossier de travail vide avant de chercher les fichiers sources.
- Hypothèse fausse sur la structure de répertoire (`files/` inexistant localement), nécessitant une recherche système (`find`).

## État actuel
- Archives décompressées et documentations (`OPERATIONS.md`, `recorder.py`) lues.
- Le token est dérivé de deux parts (north/south) stockées dans la base.
- Le WAL (`catalog.db-wal`) est critique : il contient l'historique des transactions potentiellement non checkpointées avant la panne de courant.

## Prochaines pistes
- Parser le fichier `catalog.db-wal` pour extraire les valeurs `north` et `south` de chaque transaction.
- Itérer sur les paires trouvées pour générer le token et tenter de déchiffrer `capsule.json`.
- Vérifier la cohérence des transactions "validées" selon la règle de l'opérateur.


---
## Résumé au tour 20 (02:18:17)

## Fait
- **Logique comprise** : `token = north XOR south` (2 shares de 32 octets) via `recorder.py`.
- **Structure identifiée** : Base SQLite avec tables `north`, `south`, `control`. WAL contient 39 frames (page size 1024).
- **Données brutes** : Marqueurs "CSAW" localisés dans le WAL, en-têtes de frames analysés.

## Échecs / impasses
- **Parseur WAL** : L'outil `parse_wal` n'a pas extrait les valeurs `north`/`south` directement.
- **Interprétation hex** : Les motifs `03db`, `03f1` sont des références de page, pas les clés de 32 octets recherchées.
- **Extraction** : Pas encore isolé les blobs de données chiffrées dans le flux binaire du WAL.

## État actuel
- **Contexte** : On sait que les transactions sont stockées dans le WAL et que le token final débloque `capsule.json`.
- **Données** : `catalog.db` contient l'état actuel, mais l'historique des transactions (et potentiellement le token valide) est dans le WAL.
- **Blocage** : On a la structure du fichier WAL, mais pas le mapping exact pour lire les BLOBs de 32 octets.

## Prochaines pistes
- **Scripting WAL** : Itérer manuellement les frames pour trouver des séquences de 32 octets non nulles après les en-têtes de transaction.
- **Vérification DB** : Tester si les shares actuels dans `catalog.db` suffisent pour déverrouiller `capsule.json` (état final).
- **Reconstruction** : Si nécessaire, reconstruire l'état transactionnel en appliquant les changements du WAL sur la base.


---
## Résumé au tour 30 (02:21:16)

## Fait
- **Environnement :** Correction du chemin de travail (fichiers déjà présents dans le répertoire courant, pas `/tmp/ctf`).
- **Analyse cryptographique :** Identification de `capsule.json` (chiffrement avec nonce et ciphertext).
- **Analyse DB :** Identification des tables SQLite (`north`, `south`, `control`, `maintenance`) et de la présence d'un fichier WAL actif.
- **Forensique WAL :** Parsing du header du WAL (Magic `0x377f0682`, Page size 1024 octets, 39 frames). Repérage de zones de données non nulles dans les frames.

## Échecs / impasses
- **Chemin initial :** Hypothèse fausse sur le dossier de travail (`/tmp/ctf` inexistant).
- **Fichiers docs :** `recorder.py` et `OPERATIONS.md` lus mais résultats vides ou non exploités pour l'instant.
- **Extraction WAL :** La logique d'extraction des blobs depuis les frames WAL est en cours de validation (les offsets 980+ semblent prometteurs mais la structure exacte du BLOB SQLite dans le WAL doit être confirmée).

## État actuel
- **Données clés :** `capsule.json` (chiffré), `catalog.db` (copie), `catalog.db-wal` (contient les modifications).
- **Logique de résolution :** La clé de déchiffrement dépend de `SHA256(DOMAIN + (north XOR south))`.
- **Données brutes :** Les tables `north` et `south` contiennent des BLOBs. Le WAL contient les versions modifiées de ces données.
- **Blocage :** Les valeurs `north` et `south` sont visibles en hex dans les logs partiels mais pas encore extraites proprement en binaire pour l'opération XOR.

## Prochaines pistes
- **Script d'extraction :** Finaliser le script Python pour extraire les 32 octets des BLOBs `north` et `south` directement depuis les frames du WAL.
- **Recherche du DOMAIN :** Vérifier la table `control` ou les métadonnées pour trouver la chaîne `DOMAIN` nécessaire au hachage.
- **Calcul et Déchiffrement :** Effectuer le XOR, générer la clé SHA256, et tenter de déchiffrer `capsule.json` (probablement AES-GCM).


---
## Résumé au tour 40 (02:24:43)

## Fait
- **Compréhension du schéma crypto** : Identifié que la clé de déchiffrement dérive de `SHA256(DOMAIN + XOR(north, south))` puis `AESGCM`.
- **Analyse des fichiers** : Lu `recorder.py` et `OPERATIONS.md` pour valider la logique de génération des tokens.
- **Outils personnalisés** : Forgé et exécuté `extract_wal_blobs` pour scanner les pages du WAL SQLite.

## Échecs / impasses
- **Extraction brute** : L'outil `extract_wal_blobs` a détecté 474 séquences de 32 octets, mais c'était du bruit (fenêtres glissantes sur la même donnée).
- **Parsing SQLite** : Le script Python de décodage des varints n'a trouvé aucun BLOB valide (probablement un problème d'alignement ou de structure de cellule).
- **Outil standard** : `parse_wal` a affiché les pages hexadécimales mais n'a pas isolé les valeurs nommées `north` et `south`.

## État actuel
- **Données connues** : Ciphertext et nonce dans `capsule.json`, logique de dérivation de clé claire.
- **Données manquantes** : Les 2 BLOBs de 32 octets (`north` et `south`) sont présents dans `catalog.db-wal` mais non isolés.
- **Blocage** : La structure interne des cellules SQLite (payload_length, type, rowid) n'est pas encore correctement interprétée pour extraire les données brutes.

## Prochaines pistes
- **Recherche de motifs** : Faire un `grep` ou une recherche binaire pour les chaînes "north" ou "south" dans le WAL pour localiser les cellules.
- **Correction du parsing** : Réécrire le décodeur de cellules SQLite en respectant strictement le format (header de cellule + varints).
- **Alternative** : Tenter d'attacher le WAL à une base SQLite existante via la CLI pour extraire les tables directement.
