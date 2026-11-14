

---
## Résumé au tour 10 (01:33:08)

## Fait
- Localisé et copié `evidence.zip` depuis le système de fichiers dans le workdir.
- Extrait 5 fichiers : `catalog.db`, `catalog.db-wal`, `capsule.json`, `recorder.py`, `OPERATIONS.md`.
- Décrypté la logique : `token = north XOR south` (32 octets), `key = SHA256(DOMAIN + concat(tokens))`, `flag = AESGCM(key, nonce, ciphertext)`.
- Identifié les contraintes : Échantillonnage après transaction commitée, switch `armed` doit être actif.
- Analysé le schéma SQL : Tables `control` (armed), `north`/`south` (shares), `maintenance`.

## Échecs / impasses
- Workdir initial vide (fichiers du challenge non présents par défaut).
- Fichier `catalog.db-wal` introuvable après extraction (probablement checkpointé par SQLite lors de l'ouverture du DB en Python).
- Tentative de lecture binaire du WAL (`xxd`) échouée (fichier supprimé/déplacé du FS).

## État actuel
- Fichiers sources disponibles dans le workdir (`evidence.zip` intact).
- Paramètres de chiffrement connus (`capsule.json` : nonce, ciphertext).
- Logique de dérivation de clé maîtrisée.
- Historique des transactions (WAL) manquant dans l'état actuel du DB (consommé).

## Prochaines pistes
- Ré-extraire `catalog.db-wal` du zip *avant* toute ouverture Python.
- Parser manuellement le binaire du WAL pour extraire l'historique des transactions.
- Reconstruire la séquence de tokens valides (commités + armed).
- Dériver la clé et déchiffrer le flag.


---
## Résumé au tour 20 (01:36:25)

## Fait
- Extraction complète de `evidence.zip` (5 fichiers : `catalog.db`, `catalog.db-wal`, `capsule.json`, `recorder.py`, `OPERATIONS.md`).
- Compréhension logique crypto : `token = north XOR south`, `key = SHA256(DOMAIN + tokens)`, `flag = AESGCM`.
- Analyse `OPERATIONS.md` : échantillonnage après commit, switch `armed` requis.
- Extraction manuelle de `catalog.db-wal` (40904 octets) depuis le zip (fichier absent du FS initial).
- Analyse binaire WAL : Magic `0x377f0682`, Page Size 1024, ~39 frames.

## Échecs / impasses
- WAL absent du workdir initial (checkpointé par SQLite à l'ouverture du DB).
- Tentative `xxd` initiale échouée (fichier déplacé/supprimé du FS).
- Script Python de parsing WAL planté (`NameError: frame_size` non défini dans la boucle).

## État actuel
- Fichiers sources disponibles et intacts dans le workdir.
- Paramètres de chiffrement connus (`capsule.json` : nonce, ciphertext).
- Logique de dérivation de clé maîtrisée.
- `catalog.db-wal` présent et analysé (structure connue), contenu des pages (BLOBs) à extraire.

## Prochaines pistes
- Corriger script Python (`frame_size = 24 + page_size`).
- Parser les 39 frames du WAL pour extraire BLOBs (`north`, `south`, `control`).
- Reconstruire séquence de tokens (commit + armed).
- Dériver clé et déchiffrer.


---
## Résumé au tour 30 (01:41:10)

## Fait
- Extraction complète de `evidence.zip` (5 fichiers : `catalog.db`, `catalog.db-wal`, `capsule.json`, `recorder.py`, `OPERATIONS.md`).
- Compréhension logique crypto : `token = north XOR south`, `key = SHA256(DOMAIN + tokens)`, `flag = AESGCM`.
- Analyse `OPERATIONS.md` : échantillonnage après commit, switch `armed` requis.
- Analyse binaire WAL : Magic `0x377f0682`, Page Size 1024, 39 frames.
- Connexion SQLite avec WAL attaché (`catalog_work.db`) : tables `control`, `north`, `south`, `maintenance` découvertes.
- Identification d'un offset spécifique (991) dans les pages WAL contenant des candidats BLOB de 32 octets (shares).

## Échecs / impasses
- WAL absent du workdir initial (problème de gestion de fichier/checkpoint SQLite).
- Tentative `xxd` initiale échouée (fichier déplacé/supprimé du FS).
- Script Python de parsing WAL initial planté (`NameError: frame_size`).
- Recherche naïve de BLOBs dans le WAL (trop de bruit : 38k potentiels).
- État final du DB (`armed=0`) masque l'historique des transactions `armed=1` nécessaires.

## État actuel
- Fichiers sources disponibles et intacts dans le workdir.
- Paramètres de chiffrement connus (`capsule.json` : nonce, ciphertext).
- Logique de dérivation de clé maîtrisée.
- Structure WAL connue (39 frames, 1024 octets/page).
- Schéma DB connu : `control` (armed, label), `north`/`south` (share BLOB), `maintenance` (count).
- État actuel DB : `armed=0` ('standby'), mais WAL contient l'historique des pages modifiées.
- Offset 991 identifié comme emplacement probable des shares dans les pages WAL.

## Prochaines pistes
- Parser les 39 frames du WAL en ciblant l'offset 991 pour extraire les shares.
- Corréler les frames avec les états `armed=1` dans l'historique (pages `control` dans le WAL).
- Reconstruire la séquence de tokens (commit + armed) en filtrant les frames pertinentes.
- Dériver la clé et déchiffrer le flag.


---
## Résumé au tour 40 (01:46:22)

## Fait
- Extraction complète de `evidence.zip` (5 fichiers : `catalog.db`, `catalog.db-wal`, `capsule.json`, `recorder.py`, `OPERATIONS.md`).
- Logique crypto comprise : `token = north XOR south`, `key = SHA256(DOMAIN + tokens)`, `flag = AESGCM`.
- Analyse WAL confirmée : Magic `0x377f0682`, Page Size 1024, 39 frames.
- Découverte du pattern `23010300` à l'offset 1003 dans les pages WAL (contenant les shares).
- Identification des flags de transaction : 27 transactions avec flag 5 (probables commits valides).

## Échecs / impasses
- WAL absent du workdir initial (problème de gestion de fichier/checkpoint SQLite).
- Script Python de parsing WAL initial planté (`NameError: frame_size`).
- Offset de recherche initial (991) incorrect (le pattern est à 1003).
- Données de share débordent la page (1003 + 32 octets > 1024 octets/page).
- État final du DB (`armed=0`) masque l'historique des transactions `armed=1` nécessaires.

## État actuel
- Fichiers sources disponibles et intacts dans le workdir.
- Paramètres de chiffrement connus (`capsule.json` : nonce, ciphertext).
- Structure WAL connue (39 frames, 1024 octets/page, header 32 octets).
- Schéma DB connu : `control` (armed, label), `north`/`south` (share BLOB), `maintenance`.
- Share localisation : Header `23010300` + 28 octets de données, chevauchant la fin de page.

## Prochaines pistes
- Adapter l'extraction pour gérer le débordement de page (data à 1003+).
- Filtrer les 39 frames pour ne garder que les transactions avec flag 5.
- Reconstruire la séquence des shares `north` et `south` valides.
- Calculer `token = north XOR south`, dériver la clé et déchiffrer le flag.
