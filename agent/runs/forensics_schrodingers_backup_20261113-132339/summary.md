

---
## Résumé au tour 10 (13:25:32)

## Fait
- Copié `evidence.zip` depuis le dossier challenge (problème de chemin initial résolu).
- Décompressé l'archive : identifié `catalog.db`, `catalog.db-wal`, `capsule.json`, `recorder.py`, `OPERATIONS.md`.
- Compris la logique cryptographique : Token = `north XOR south` (32 octets), clé = SHA256(Domain + Tokens), chiffrement AES-GCM.
- Identifié les tables SQLite : `north`, `south`, `control`, `maintenance`.

## Échecs / impasses
- **Chemin fichier** : `ls` initial ne montrait pas `evidence.zip` (nécessité de `find`).
- **Encodage SQL** : `SELECT *` sur `north`/`south` a échoué (erreur UTF-8 sur des BLOBs).
- **Schéma DB** : Hypothèse de colonne `data` incorrecte ("no such column").

## État actuel
- Fichiers extraits et contexte lu.
- Logique de dérivation de clé comprise.
- Base de données SQLite prête à l'analyse (DB + WAL).
- Nom des colonnes dans `north` et `south` inconnu.

## Prochaines pistes
- Récupérer le schéma (`PRAGMA table_info`) pour nommer les colonnes.
- Extraire les BLOBs (hex/raw) des tables `north` et `south`.
- Analyser le fichier `catalog.db-wal` pour récupérer les états intermédiaires (avant commit).
- Reconstruire la séquence de tokens et déchiffrer `capsule.json`.


---
## Résumé au tour 20 (13:27:14)

## Fait
- Navigation vers le bon répertoire de travail et lecture des fichiers de contexte (`OPERATIONS.md`, `recorder.py`).
- Compréhension de la logique : Token = XOR(share_north, share_south), chiffré en AESGCM.
- Extraction des tables SQLite (`north`, `south`, `control`) et récupération des shares actuels (32 octets chacun).
- Identification du problème critique : le fichier `catalog.db-wal` extrait était vide (0 octets).
- Restauration du fichier WAL original (40 KB) depuis `evidence.zip`.

## Échecs / impasses
- **Hypothèse de chemin :** Tentative initiale ratée de `cd /tmp/ctf`.
- **Fichier WAL corrompu :** Confiance initiale dans le fichier `catalog.db-wal` présent dans le dossier de travail, qui s'est avéré vidé par la connexion SQLite précédente.
- **État statique :** Avoir considéré les shares de la base principale comme définitives sans vérifier l'historique des transactions dans le WAL.

## État actuel
- **Données connues :** Shares actuels de `north` et `south` (depuis `catalog.db`), `capsule.json` (chiffré), `recorder.py` (algorithme).
- **Données critiques récupérées :** Le fichier `catalog.db-wal` original est maintenant disponible et contient l'historique des écritures.
- **Logique :** Le token affiché correspond à l'état des contrôleurs après une transaction validée. Le WAL contient les pages modifiées avant le checkpoint.

## Prochaines pistes
- **Parser le WAL :** Écrire un script pour lire les pages du fichier WAL et extraire les modifications successives des tables `north` et `south`.
- **Reconstruction d'état :** Simuler l'application des transactions du WAL pour retrouver les valeurs des shares au moment de l'enregistrement.
- **Décryptage :** Calculer le XOR des shares reconstruits, puis tenter de déchiffrer `capsule.json` avec la clé dérivée.


---
## Résumé au tour 30 (13:32:12)

## Fait (actions utiles et ce qu'elles ont donné)
- **Logique crypto identifiée** : Token = XOR(north, south) ; Clé dérivée = SHA256(DOMAIN + concaténation des tokens).
- **Analyse WAL réussie** : Structure comprise (39 frames, page size 1024), pages de type table leaf (0x0d) identifiées.
- **Extraction de données** : Payloads SQLite décodés, format des shares (32 octets) repéré dans les cellules des pages 3 (north) et 4 (south).

## Échecs / impasses (ce qui n'a PAS marché — à ne pas refaire)
- **Chemin initial** : Tentative infructueuse de `cd /tmp/ctf` (dossier inexistant).
- **Extraction brute** : L'outil `extract_wal_blobs` a généré trop de faux positifs (474 blobs) sans filtrage par page.
- **Gestion de fichier** : Le fichier `catalog.db-wal` (40 KB) a disparu du listing `ls` final, risquant une perte de l'historique des transactions.

## État actuel (ce qu'on sait, fichiers/indices clés)
- **Fichiers** : `catalog.db` (5120 octets, DB principale), `capsule.json` (chiffré).
- **Schéma** : Tables `control` (état), `north`/`south` (shares BLOB 32 octets), `maintenance`.
- **Données connues** : Shares actuels extraits, mais la clé de déchiffrement nécessite l'historique complet des tokens stocké dans le WAL.

## Prochaines pistes
- **Localisation WAL** : Retrouver `catalog.db-wal` ou vérifier si les données ont été checkpointées dans `catalog.db`.
- **Parsing séquentiel** : Scripter l'extraction des pages 3 et 4 pour chaque frame du WAL afin de reconstruire la chronologie des shares.
- **Déchiffrement** : Calculer la clé SHA256 avec les tokens historiques et tenter de déchiffrer `capsule.json` en AESGCM.


---
## Résumé au tour 40 (13:33:41)

## Fait
- **Exploration du dossier** : Identification des fichiers clés (`catalog.db`, `capsule.json`, `evidence.zip`, scripts Python).
- **Analyse de la base de données** : Récupération du schéma et des données actuelles de `catalog.db` (tables `north` et `south` contenant des shares hexadécimaux).
- **Récupération du WAL** : Extraction réussie de `catalog.db-wal` depuis `evidence.zip` (fichier manquant dans le répertoire de travail).
- **Vérification d'intégrité** : Confirmation que le fichier WAL est valide (`SQLite Write-Ahead Log`).

## Échecs / impasses
- **Hypothèse de fichier manquant** : Avoir cru que le WAL était corrompu ou perdu alors qu'il était simplement archivé dans `evidence.zip`.
- **Lecture SQL directe** : Interroger `catalog.db` avec `sqlite3` n'a donné que l'état *actuel* des tables, masquant l'historique nécessaire à la reconstruction de la clé.
- **Analyse binaire brute** : L'inspection manuelle avec `xxd` du WAL est lente sans script de parsing dédié.

## État actuel
- **Chiffrement** : `capsule.json` contient un ciphertext et un nonce (AES probablement).
- **Clés partielles** : On possède les shares actuels de `north` et `south`, mais il manque les versions historiques pour reconstruire le secret.
- **Preuve historique** : Le fichier `catalog.db-wal` (40904 octets) contient les transactions passées modifiant les tables `north` et `south`.
- **Contexte** : Probable schéma de partage de secret (Shamir) nécessitant plusieurs versions de shares pour dériver la clé maîtresse.

## Prochaines pistes
- **Parsing du WAL** : Écrire un script Python pour extraire les pages de type "table leaf" (0x0d) du fichier WAL et récupérer les anciennes valeurs BLOB.
- **Reconstruction** : Combiner les shares historiques extraits avec les shares actuels pour former la clé de déchiffrement.
- **Déchiffrement** : Utiliser la clé reconstruite pour décrypter le contenu de `capsule.json`.
