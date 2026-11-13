

---
## Résumé au tour 10 (23:04:45)

## Fait
- **Localisation du fichier :** Contournement du chemin attendu (`/challenge/files`) via `find`, récupération de `evidence.zip` depuis `/home/...`.
- **Extraction :** Décompression réussie de l'archive contenant 5 fichiers (DB, logs, scripts).
- **Compréhension du mécanisme :** Lecture de `OPERATIONS.md` révélant que le token est le XOR de deux parts (Nord/Sud) mises à jour par transaction.

## Échecs / impasses
- **Hypothèse de chemin :** Perte de temps initiale à chercher `/challenge/files/evidence.zip` qui n'existait pas.
- **Script incomplet :** `recorder.py` s'arrête en plein milieu de la fonction `token`, la logique de chiffrement AESGCM n'est pas encore fully implémentée.

## État actuel
- **Fichiers clés :** `catalog.db` (base SQLite) et `catalog.db-wal` (journal de transaction) sont extraits et prêts à l'analyse.
- **Logique :** On sait qu'il faut extraire les valeurs "North" et "South" des transactions validées ("committed") pour calculer le token.
- **Données :** `capsule.json` et `recorder.py` contiennent probablement les clés ou le format exact des shares.

## Prochaines pistes
- **Analyse SQLite :** Ouvrir `catalog.db` (et le WAL) pour lister les transactions et extraire les colonnes contenant les shares.
- **Compléter le script :** Récupérer la fin de `recorder.py` ou déduire la logique AESGCM pour valider le token.
- **Inspection JSON :** Lire `capsule.json` pour vérifier s'il contient des clés de décryptage ou des métadonnées manquantes.


---
## Résumé au tour 20 (23:06:45)

## Fait
- **Analyse du code** : Compris le mécanisme de `recorder.py` (token = XOR des shares North/South, chiffrement AESGCM).
- **Documentation** : `OPERATIONS.md` confirme que l'enregistrement se fait après chaque transaction validée (committed).
- **Base de données** : Structure de `catalog.db` cartographiée (tables `north`, `south`, `control`) et shares actuels extraits.

## Échecs / impasses
- **Fichier WAL** : `catalog.db-wal` listé au début mais disparu après la première connexion `sqlite3.connect` (probable checkpoint automatique).
- **Déchiffrement** : Tentative de décryptage de `capsule.json` bloquée car le token actuel ne correspond peut-être pas à celui de la transaction enregistrée.
- **Accès direct** : Lecture binaire du WAL échouée deux fois (`FileNotFoundError`).

## État actuel
- **Données connues** : Shares North et South actuels (blobs de 32 octets), `nonce` et `ciphertext` de `capsule.json`.
- **Données manquantes** : Historique des transactions validées (contenu du WAL) pour retrouver le token exact au moment de l'enregistrement.
- **Environnement** : Fichiers principaux (`recorder.py`, `catalog.db`, `capsule.json`, `evidence.zip`) disponibles dans le dossier de travail.

## Prochaines pistes
- **Inspecter `evidence.zip`** : Chercher une copie du WAL ou des snapshots de la base de données.
- **Forensique DB** : Parser les octets bruts de `catalog.db` pour tenter de récupérer des frames WAL résiduelles si elles n'ont pas été écrasées.
- **Brute-force logique** : Si le WAL est perdu, vérifier si les transactions peuvent être déduites via les logs ou l'état `maintenance`.


---
## Résumé au tour 30 (23:08:16)

## Fait (actions utiles et ce qu'elles ont donné)
- **Analyse du code :** Compris le mécanisme de chiffrement via `recorder.py` et `OPERATIONS.md` (Token = XOR des shares, Clé = SHA256(DOMAIN + historique des tokens)).
- **Localisation des fichiers :** Identifié que les fichiers sont à la racine du workdir, pas dans un sous-dossier `files/`.
- **Récupération de données :** Extrait `evidence.zip` qui contenait la copie intacte de `catalog.db-wal`, absente du système de fichiers actif.

## Échecs / impasses (ce qui n'a PAS marché — à ne pas refaire)
- **Chemin de fichier :** Perte de temps à chercher `files/evidence.zip` alors qu'il était dans `.`.
- **Manipulation directe du WAL :** Tentative de copier ou lire `catalog.db-wal` dans l'environnement live (il disparaissait ou était verrouillé).
- **Hypothèse de stabilité :** Avoir cru que le WAL était accessible directement sans passer par l'archive de preuve.

## État actuel (ce qu'on sait, fichiers/indices clés)
- **Logique :** Il faut reconstruire l'historique des tokens pour dériver la clé AESGCM.
- **Données :** `capsule.json` contient le ciphertext et le nonce. `evidence_extracted/catalog.db-wal` contient les pages SQLite avec les shares.
- **Outils :** Fichiers extraits prêts pour analyse binaire/SQL.

## Prochaines pistes
- **Parsing du WAL :** Écrire un script Python pour lire les frames du fichier `catalog.db-wal` extrait.
- **Extraction des shares :** Identifier les pages SQLite contenant les valeurs North et South.
- **Déchiffrement :** Calculer la clé dérivée et tenter de déchiffrer `capsule.json`.


---
## Résumé au tour 40 (23:10:11)

## Fait (actions utiles et ce qu'elles ont donné)
- **Analyse du code :** Compris la logique de génération de clé (SHA256(DOMAIN + tokens)) et de déchiffrement (AESGCM) via `OPERATIONS.md` et `recorder.py`.
- **Extraction de données :** Récupéré `ciphertext` et `nonce` dans `capsule.json`.
- **Outil personnalisé :** Forgé et exécuté `parse_wal` pour lire le fichier WAL.
- **Correction de chemin :** Localisé le bon fichier WAL dans `evidence_extracted/` après erreur initiale.

## Échecs / impasses (ce qui n'a PAS marché — à ne pas refaire)
- **Chemin de fichier :** Avoir supposé que `catalog.db-wal` était à la racine (erreur `FileNotFoundError`).
- **Parsing brut :** L'outil actuel affiche un dump hexadécimal brut des pages sans extraire directement les valeurs `north` et `south` (nécessite un post-traitement).

## État actuel (ce qu'on sait, fichiers/indices clés)
- **Fichiers clés :** `capsule.json` (chiffrement), `evidence_extracted/catalog.db-wal` (données brutes).
- **Structure WAL :** Fichier valide (Magic `377f0682`), 39 frames détectées, taille de page 1024.
- **Logique :** Les shares (north/south) sont stockés dans les pages SQLite du WAL. Les tokens sont le XOR de ces shares.

## Prochaines pistes
- **Affiner le parser :** Modifier `parse_wal` pour extraire les valeurs hexadécimales spécifiques des colonnes `north` et `south` au lieu du dump brut.
- **Calculer la clé :** Concaténer les tokens extraits et générer la clé SHA256.
- **Déchiffrer :** Utiliser la clé et le nonce pour déchiffrer le `ciphertext` de `capsule.json`.
