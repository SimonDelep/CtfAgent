

---
## Résumé au tour 10 (16:38:04)

## Fait
- Localisé et copié `evidence.zip` depuis le dossier source (évité les copies temporaires).
- Extrait l'archive : base SQLite (`catalog.db` + `.wal`), script `recorder.py`, `capsule.json`, `OPERATIONS.md`.
- Compris la logique via `OPERATIONS.md` : Token = XOR(Share_Nord, Share_Sud), échantillonnage après commit transactionnel.

## Échecs / impasses
- Démarrage dans `/work` vide (temps perdu à lister des dossiers vides).
- Multiples copies de `evidence.zip` trouvées via `find` (risque de travailler sur une version modifiée).
- Pas encore d'analyse binaire ou SQL effectuée (phase d'exploration uniquement).

## État actuel
- **Fichiers clés :** `catalog.db` (état persistant), `catalog.db-wal` (modifications en cours), `capsule.json`.
- **Indices :** Les contrôleurs affichent des parts de 32 octets. Le WAL contient des pages écrites mais pas forcément committées dans le DB principal.
- **Objectif :** Récupérer les parts valides (post-commit) pour calculer le XOR.

## Prochaines pistes
- Inspecter le schéma de `catalog.db` (tables, colonnes contenant les shares).
- Comparer les données dans `catalog.db` vs `catalog.db-wal` pour identifier les transactions validées.
- Écrire un script Python pour extraire les shares et calculer le token final.
- Vérifier `capsule.json` pour des métadonnées de timestamp ou d'ID.


---
## Résumé au tour 20 (16:41:10)

## Fait (actions utiles et ce qu'elles ont donné)
*   **Extraction des preuves :** Décompression de `evidence.zip`, rendant accessibles `catalog.db`, `catalog.db-wal` et les scripts.
*   **Compréhension du challenge :** Lecture de `OPERATIONS.md` et `recorder.py` confirmant la logique : Token = XOR(north, south), Clé = SHA256(DOMAIN + tous les tokens), Ciphertext = AES-GCM.
*   **Analyse structurelle :** Inspection du schéma SQLite (tables `north`, `south`, `control`) et du header du fichier WAL (39 frames, page size 1024).

## Échecs / impasses (ce qui n'a PAS marché — à ne pas refaire)
*   **Chemin de fichiers :** Tentatives de lecture initiales (`read_file`) échouées car les fichiers étaient dans `evidence.zip` et non dans le workdir immédiat.
*   **Extraction brute de blobs :** L'outil `extract_wal_blobs` a généré trop de faux positifs (474 blobs potentiels) sans contexte transactionnel, rendant l'analyse manuelle difficile.
*   **Accès WAL direct :** Lecture du WAL sans vérifier son existence avant extraction du zip.

## État actuel (ce qu'on sait, fichiers/indices clés)
*   **Données disponibles :** `catalog.db` (état actuel), `catalog.db-wal` (historique des transactions), `capsule.json` (nonce + ciphertext).
*   **Logique validée :** Le `recorder.py` définit `SHARE_SIZE=32` et `DOMAIN`. Le token est enregistré après chaque transaction *commitée*.
*   **Problème identifié :** Le DB principal contient des shares, mais le WAL contient l'historique des mises à jour. Il faut identifier les pages avec `commit flag` valide pour reconstruire la séquence de tokens.

## Prochaines pistes
*   **Parser le WAL proprement :** Écrire un script pour extraire uniquement les pages de type table leaf (0x0d) avec un flag de commit valide, en ignorant les pages intermédiaires.
*   **Reconstruire la séquence :** Extraire les valeurs `north` et `south` de chaque transaction commitée dans l'ordre chronologique.
*   **Calculer la clé :** Générer la clé de déchiffrement via SHA256(DOMAIN + concaténation des tokens) et tenter de décrypter `capsule.json`.


---
## Résumé au tour 30 (16:43:20)

## Fait
- **Analyse source :** Compris le mécanisme de `recorder.py` (Token = `north` XOR `south`, chiffrement AESGCM) et le rôle du WAL dans `OPERATIONS.md`.
- **Cible identifiée :** `capsule.json` contient le ciphertext et le nonce à déchiffrer.
- **Base de données :** Schéma SQLite inspecté (tables `north`, `south`, `control`).
- **Environnement :** Extraction du `evidence.zip` confirmée, fichiers accessibles.

## Échecs / impasses
- **Extraction WAL brute :** L'outil `extract_wal_blobs` a retourné 474 blobs potentiels, trop de bruit pour un tri manuel.
- **Script Python :** Échec initial (`FileNotFoundError`) dû à un chemin relatif incorrect vers `catalog.db-wal`.
- **Parsing WAL :** Difficulté à isoler les valeurs de partage valides directement des frames sans logique de transaction.

## État actuel
- **Logique de résolution :** Il faut récupérer les valeurs de partage (`north`/`south`) de chaque transaction commitée dans le WAL.
- **Données :** Le fichier WAL (`catalog.db-wal`) est présent, les pages de type table leaf (0x0d) contiennent les données BLOB.
- **Blocage :** Nécessité de mapper correctement les frames WAL aux valeurs `north` et `south` pour reconstruire les tokens.

## Prochaines pistes
- **Correction de chemin :** Relancer le script Python en spécifiant le chemin absolu ou relatif correct vers le WAL.
- **Parsing ciblé :** Écrire un parser pour lire uniquement les pages 0x0d et extraire les BLOBs de 32 octets correspondant aux colonnes `north` et `south`.
- **Déchiffrement :** Itérer sur les paires de shares extraites pour tenter de déchiffrer `capsule.json` avec la clé dérivée du token.


---
## Résumé au tour 40 (16:46:33)

## Fait (actions utiles et ce qu'elles ont donné)
- Extraction réussie de `evidence.zip` (après correction de la commande `unzip -d .`).
- Identification de la structure SQLite (`catalog.db` + `catalog.db-wal`) et des fichiers annexes.
- Compréhension de la logique : `token = north XOR south`, clé = `SHA256(DOMAIN + tokens)`.
- Forge de l'outil `wal_parser` pour extraire les BLOBs du WAL.

## Échecs / impasses (ce qui n'a PAS marché — à ne pas refaire)
- Commande `xxd catalog.db-wal` lancée avant extraction complète (fichier manquant).
- Commande `unzip` simple sans destination explicite (fichiers invisibles dans le listing immédiat).
- Lecture directe des fichiers texte (`recorder.py`, `OPERATIONS.md`) sans affichage de contenu dans le trace (nécessite vérification de taille/chemin).

## État actuel (ce qu'on sait, fichiers/indices clés)
- Fichiers disponibles : `catalog.db`, `catalog.db-wal`, `capsule.json`, `recorder.py`, `OPERATIONS.md`.
- Objectif : Parser le WAL pour récupérer les BLOBs `north` et `south` dans l'ordre des transactions commitées.
- Outil `wal_parser` prêt à être exécuté sur `catalog.db-wal`.

## Prochaines pistes
- Exécuter `wal_parser` pour extraire les valeurs `north` et `south`.
- Calculer les tokens et la clé de déchiffrement finale.
- Déchiffrer `capsule.json` pour obtenir le flag.
