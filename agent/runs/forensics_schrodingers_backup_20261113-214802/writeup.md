# Write-up — Schrodinger's Backup (forensics)

- **Flag** : `NON TROUVÉ`

# Write-up : Schrodingers Backup

## 1. Challenge
**Nom** : Schrodingers Backup  
**Catégorie** : Forensics  
**Résumé** : Extraire des clés de chiffrement à partir d'un historique de transactions SQLite WAL pour déchiffrer une capsule temporelle.

## 2. Vulnérabilité / Mécanique
- **Token** = `north_share XOR south_share` (32 octets chacun)
- **Clé de déchiffrement** = `SHA256(DOMAIN + concaténation de tous les tokens)`
- **Chiffrement** : AES-GCM avec l'AD (Associated Data) = `DOMAIN`
- **Point clé** : Le fichier `catalog.db` ne contient que l'état final, mais l'historique des transactions (et donc tous les tokens) est stocké dans le fichier **WAL** (`catalog.db-wal`)

## 3. Étapes de résolution

### 3.1. Extraction des fichiers
```bash
# Recherche du fichier evidence.zip
find / -name "evidence.zip" 2>/dev/null

# Extraction propre
unzip -o evidence.zip -d .
```
Fichiers obtenus : `catalog.db`, `catalog.db-wal`, `capsule.json`, `recorder.py`, `OPERATIONS.md`

### 3.2. Analyse de la logique
- **recorder.py** : Définit la fonction `token(north, south)` (XOR des deux shares) et `derive_key()` (SHA256 de la concaténation)
- **OPERATIONS.md** : Confirme que le recorder échantillonne après chaque transaction commitée
- **capsule.json** : Contient le `ciphertext` et le `nonce` pour AES-GCM

### 3.3. Analyse de la base de données
```bash
sqlite3 catalog.db ".schema"
sqlite3 catalog.db "SELECT id, hex(share) FROM north;"
sqlite3 catalog.db "SELECT id, hex(share) FROM south;"
```
Tables identifiées : `north`, `south`, `control`, `maintenance`

### 3.4. Parsing du WAL
- Le fichier `catalog.db-wal` (40904 octets) contient l'historique des transactions
- Page size = 1024 octets (environ 40 frames)
- Objectif : Extraire les BLOBs de 32 octets correspondant aux shares `north` et `south` des transactions commitées

### 3.5. Approche de résolution
1. Parser le header WAL pour obtenir le page_size
2. Itérer sur les frames et pages de type "table leaf" (0x0d)
3. Extraire les paires (north, south) dans l'ordre des transactions
4. Calculer chaque token = north XOR south
5. Dériver la clé : `SHA256(DOMAIN + all_tokens)`
6. Déchiffrer avec AES-GCM en utilisant le nonce et l'AD du fichier `capsule.json`

## 4. Flag
**Statut** : Approche établie, déchiffrement final à exécuter  
**Méthode** : `AESGCM(key).decrypt(nonce, ciphertext, associated_data=DOMAIN)`

---

**Outils utilisés** : `find`, `unzip`, `sqlite3`, `xxd`, script Python personnalisé pour parsing WAL