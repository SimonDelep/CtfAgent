# Write-up — Schrodinger's Backup (forensics)

- **Flag** : `NON TROUVÉ`

# Write-up CTF : Schrodingers Backup

## 1. Challenge
- **Nom** : Schrodingers Backup
- **Catégorie** : Forensics
- **Résumé** : Extraire l'historique des tokens d'une capsule temporelle depuis un fichier SQLite WAL non checkpointé.

## 2. Vulnérabilité / mécanique
- **Faille** : SQLite WAL (Write-Ahead Log) non checkpointé contenant des transactions historiques.
- **Mécanique** : 
  - Token = XOR des shares `north` et `south` (32 octets chacun)
  - La clé de déchiffrement = SHA256(DOMAIN + tous les tokens historiques)
  - Le WAL contient les transactions avant leur écriture dans le DB principal

## 3. Étapes de résolution

### 3.1 Localisation des fichiers
```bash
find / -name "evidence.zip" 2>/dev/null
# Trouvé dans : /home/etudiantelambda/Documents/CSAW_LLM_2026-BTN-DLP/CtfAgent/CSAW-Quals/forensics/schrodingers_backup/files/evidence.zip
```

### 3.2 Extraction et analyse
```bash
cp evidence.zip . && unzip -o evidence.zip
# Contenu : catalog.db, catalog.db-wal, capsule.json, recorder.py, OPERATIONS.md
```

### 3.3 Analyse de la base SQLite
```python
import sqlite3
conn = sqlite3.connect('catalog.db')
cursor = conn.cursor()
cursor.execute("SELECT name FROM sqlite_master WHERE type='table';")
# Tables : control, north, south, maintenance
```

### 3.4 Structure des données
- **control** : état armé/désarmé (armed=0 pour standby)
- **north/south** : shares de 32 octets pour chaque token
- **maintenance** : compteur de transactions (pulse=25)

### 3.5 Mécanisme de récupération
1. Lire les transactions du WAL avant checkpoint
2. Extraire les paires (north, south) de chaque transaction
3. Calculer token = XOR(north, south) pour chaque transaction
4. Dériver la clé : `SHA256(DOMAIN + tokens_historiques)`
5. Déchiffrer `capsule.json` avec AESGCM

## 4. Flag
```
# À extraire après déchiffrement de capsule.json
# Format attendu : CSAW{...}
```

## Points clés
- Le fichier WAL (`catalog.db-wal`, 40904 octets) contient les transactions non checkpointées
- SQLite peut consommer le WAL lors de l'ouverture, nécessitant une copie préalable
- La documentation `OPERATIONS.md` explique que le recorder ne capture que les transactions **commitées** quand le système est **armé**