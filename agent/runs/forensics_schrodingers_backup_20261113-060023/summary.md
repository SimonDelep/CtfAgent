

---
## Résumé au tour 10 (06:01:52)

## Fait
- **Localisation des fichiers :** Contourné le dossier manquant via `find` pour récupérer `evidence.zip`.
- **Extraction :** Archive décompressée avec succès (5 fichiers : DB, WAL, JSON, script, doc).
- **Analyse préliminaire :** Compréhension du mécanisme via `OPERATIONS.md` et `recorder.py` (Token = XOR des parts Nord/Sud).

## Échecs / impasses
- **Chemin de fichier :** Hypothèse erronée sur `/challenge/files/` (dossier vide au départ).
- **Navigation :** Perte de temps à lister le dossier courant avant de chercher le zip ailleurs.
- **À éviter :** Ne pas supposer que les assets sont dans le dossier de travail initial.

## État actuel
- **Données brutes :** `catalog.db` et `catalog.db-wal` contiennent probablement l'historique des transactions (parts Nord/Sud).
- **Cible :** `capsule.json` contient le flag chiffré (AESGCM) avec un nonce connu.
- **Logique :** Il faut reconstruire l'état final du "display" (XOR des parts) pour obtenir la clé de déchiffrement.

## Prochaines pistes
- **Inspection DB :** Lancer `sqlite3 catalog.db` pour voir le schéma et les tables.
- **Extraction :** Récupérer les valeurs `north` et `south` de la dernière transaction validée.
- **Crypto :** Calculer le token (XOR) et tenter de déchiffrer `capsule.json`.


---
## Résumé au tour 20 (06:03:44)

## Fait
- **Analyse des fichiers** : Dézippé `evidence.zip`, lu `OPERATIONS.md` et `recorder.py`.
- **Compréhension du crypto** : Token = `XOR(north_share, south_share)` (32 bytes chacun). Clé = `SHA256(DOMAIN + concat(tokens))`. Chiffrement = AES-256-GCM.
- **Base de données** : Identifié le schéma (`north`, `south`, `control`, `maintenance`). Extrait les shares actuels de `catalog.db`.
- **WAL** : Localisé et initialisé l'analyse de `catalog.db-wal` (39 frames détectées, page size 1024).

## Échecs / impasses
- **Checkpoint SQLite** : Ouvrir `catalog.db` avec SQLite a fusionné le WAL dans la DB, effaçant l'historique des transactions nécessaires (seule la dernière état est visible).
- **Encodage BLOB** : Premier `SELECT` échoué via CLI à cause des bytes bruts (résolu via Python).
- **Perte de contexte** : Le fichier `catalog.db-wal` a disparu du dossier racine après le premier accès, nécessitant une extraction propre dans `workdir/`.

## État actuel
- **Données connues** :
  - `capsule.json` : Ciphertext et nonce disponibles.
  - `recorder.py` : Domaine constant `b"csaw-2026/schrodingers-backup/v1\x00"`.
  - Shares actuels (post-checkpoint) : `north` et `south` identifiés.
- **Données manquantes** : La séquence complète des `north` et `south` shares de *toutes* les transactions validées (stockées dans le WAL avant le checkpoint).
- **Outil** : `parse_wal` a extrait les pages brutes, mais le lien entre les frames et les lignes SQL n'est pas encore établi.

## Prochaines pistes
- **Parsing WAL manuel** : Écrire un script pour itérer sur les 39 frames du WAL et identifier les pages contenant les BLOBs des tables `north` et `south`.
- **Reconstruction chronologique** : Extraire les valeurs de shares dans l'ordre des transactions validées (repérer les en-têtes de commit).
- **Calcul de la clé** : Générer la chaîne de tokens, hasher avec SHA256, et tenter le déchiffrement de `capsule.json`.


---
## Résumé au tour 30 (06:05:27)

## Fait (actions utiles et ce qu'elles ont donné)
- **Localisation des fichiers :** Utilisation de `find` pour localiser `evidence.zip` après échec des chemins relatifs initiaux.
- **Préparation de l'environnement :** Copie des fichiers sources (`schrodingers_backup/files`) dans le répertoire de travail.
- **Extraction :** Décompression de `evidence.zip` révélant 5 fichiers (base de données, script, documentation).
- **Vérification :** Confirmation de la présence des fichiers via `find . -type f` (plus fiable que `ls` dans ce contexte).

## Échecs / impasses (ce qui n'a PAS marché — à ne pas refaire)
- **Cheminement initial :** Tentative d'accès à `files/` et `/challenge/` qui n'existaient pas dans le contexte actuel.
- **Listing aveugle :** `ls -la` répété sans afficher de contenu immédiat, obligeant à utiliser `find` pour voir la structure.
- **Gestion des chemins :** Duplication des fichiers (racine et `./workdir/`) après extraction, créant une légère confusion sur l'emplacement canonique.

## État actuel (ce qu'on sait, fichiers/indices clés)
- **Challenge :** Forensics (Schrodingers Backup).
- **Artefacts principaux :**
  - `catalog.db` : Base de données SQLite.
  - `catalog.db-wal` : Journal de transactions (Write-Ahead Log), potentiellement crucial.
  - `capsule.json` : Métadonnées ou configuration.
  - `recorder.py` & `OPERATIONS.md` : Documentation du système et logique d'écriture.
- **Contexte :** Les fichiers datent du 01/01/2026, suggérant un scénario temporel ou de backup.

## Prochaines pistes
- **Analyse textuelle :** Lire `OPERATIONS.md` et `recorder.py` pour comprendre le schéma de la base de données.
- **Inspection SQL :** Ouvrir `catalog.db` avec `sqlite3` pour lister les tables et le contenu.
- **Forensique WAL :** Examiner `catalog.db-wal` pour récupérer des données écrites mais non checkpointées (données "fantômes").
- **JSON :** Analyser `capsule.json` pour des indices sur le contenu ou le flag.


---
## Résumé au tour 40 (06:07:28)

## Fait
- **Logique cryptographique comprise** : Token = XOR(north, south), Clé = SHA256(DOMAIN + tokens), Capsule = AES-256-GCM.
- **Extraction des données** : Récupération des shares `north` et `south` actuels depuis `catalog.db` (format hex).
- **Calcul intermédiaire** : Token actuel généré à partir des shares DB.
- **Analyse WAL** : Identification de la structure SQLite WAL et extraction de blobs potentiels (39 frames, 474 blobs suspects).

## Échecs / impasses
- **Bruit dans le WAL** : L'outil `extract_wal_blobs` retourne trop de faux positifs (décalages de lecture).
- **Structure WAL opaque** : `parse_wal` montre des pages de type `0x0d` mais ne isole pas clairement les valeurs de shares.
- **Fichier manquant** : `catalog.db-wal` a disparu lors du dernier `xxd` (probable checkpoint ou déplacement), coupant l'accès direct aux transactions non commitées.

## État actuel
- **Chiffrement prêt** : On sait comment décrypter `capsule.json` si on a la bonne clé.
- **Données DB connues** : On a l'état *actuel* de la base (shares, schema), mais l'historique (WAL) est critique.
- **Indice manquant** : Il faut lier les transactions WAL au champ `control.armed` pour valider quels tokens compter dans la clé SHA256.

## Prochaines pistes
- **Récupérer le WAL** : Vérifier si le fichier a été renommé, ou si les données ont été checkpointées dans `catalog.db` (re-lire la DB).
- **Analyse temporelle** : Croiser les timestamps des frames WAL avec l'état `armed` du controller.
- **Brute-force sélectif** : Si le WAL est perdu, tester si les shares actuels suffisent, ou chercher des backups temporaires.
