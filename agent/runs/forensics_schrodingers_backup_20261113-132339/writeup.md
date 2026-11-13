# Write-up — Schrodinger's Backup (forensics)

- **Flag** : `NON TROUVÉ`

# Schrodinger's Backup

## Challenge
**Nom** : Schrodinger's Backup  
**Catégorie** : Forensics  
**Résumé** : Récupérer l'historique complet des transactions d'une capsule temporelle à partir d'une base SQLite avec WAL.

## Vulnérabilité / mécanique
La faille réside dans le **Write-Ahead Log (WAL)** de SQLite. Les transactions sont écrites dans le WAL avant d'être checkpointées dans le fichier principal. Après une panne de courant, le WAL contient des états intermédiaires validés mais non consolidés. Chaque transaction commitée dans le WAL représente un état réel de l'affichage (token = XOR des shares north/south).

## Étapes de résolution

1. **Localisation des fichiers** : `evidence.zip` trouvé dans le dossier du challenge, copié dans le workdir.

2. **Extraction de l'archive** :
   ```bash
   unzip -o evidence.zip
   ```
   Contenu : `catalog.db`, `catalog.db-wal`, `capsule.json`, `recorder.py`, `OPERATIONS.md`

3. **Problème détecté** : Le fichier `catalog.db-wal` extrait faisait 0 octet (SQLite l'avait checkpointé). Ré-extraction directe depuis l'archive :
   ```bash
   unzip -o evidence.zip catalog.db-wal
   ```
   Taille correcte : 40904 octets.

4. **Analyse de la base SQLite** :
   ```python
   import sqlite3
   conn = sqlite3.connect('catalog.db')
   cursor = conn.cursor()
   cursor.execute("SELECT name FROM sqlite_master WHERE type='table';")
   # Tables : control, north, south, maintenance
   ```

5. **Extraction des shares** :
   ```python
   cursor.execute("SELECT share FROM north;")
   north_share = cursor.fetchone()[0]  # 32 bytes
   cursor.execute("SELECT share FROM south;")
   south_share = cursor.fetchone()[0]  # 32 bytes
   ```

6. **Logique de décodage** (d'après `recorder.py` et `OPERATIONS.md`) :
   - Token = `north_share XOR south_share`
   - Clé de déchiffrement = `SHA256(DOMAIN + tous les tokens concaténés)`
   - Capsule chiffrée en AES-GCM (dans `capsule.json`)
   - Le WAL doit être parsé pour extraire **tous** les tokens des transactions commitées

## Flag
`csaw{...}` (à obtenir après extraction complète des tokens depuis le WAL et déchiffrement de la capsule)

---

**Note** : La trajectoire s'arrête avant le parsing final du WAL. La solution complète nécessite d'extraire chaque page du WAL, reconstruire l'historique des transactions, calculer tous les tokens, puis déchiffrer `capsule.json`.