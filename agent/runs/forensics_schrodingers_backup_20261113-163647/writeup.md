# Write-up — Schrodinger's Backup (forensics)

- **Flag** : `NON TROUVÉ`

# Schrodingers Backup - Write-up

## 1. Challenge
**Nom** : Schrodingers Backup  
**Catégorie** : Forensics  
**Résumé** : Extraire des shares cachées dans un WAL SQLite pour reconstruire un token et déchiffrer une capsule.

---

## 2. Vulnérabilité / Mécanique
Le challenge exploite la **mécanique SQLite WAL (Write-Ahead Log)** :
- Le fichier `catalog.db` contient l'état final de la base
- Le fichier `catalog.db-wal` contient des transactions non checkpointées (modifications non écrites dans le DB principal)
- Le token = `XOR(north_share, south_share)` (32 octets chacun)
- Le `capsule.json` contient un ciphertext chiffré en AES-256-GCM, la clé étant dérivée de `SHA256(DOMAIN + tous les tokens enregistrés)`
- Seules les transactions **commitées** (commit flag ≠ 0) dans le WAL sont valides

---

## 3. Étapes de résolution

### Étape 1 : Extraction des fichiers
```bash
cp /home/etudiantelambda/Documents/CSAW_LLM_2026-BTN-DLP/CtfAgent/CSAW-Quals/forensics/schrodingers_backup/files/evidence.zip .
unzip -o evidence.zip
```
Fichiers obtenus : `catalog.db`, `catalog.db-wal`, `capsule.json`, `recorder.py`, `OPERATIONS.md`

### Étape 2 : Analyse de la base SQLite
```python
import sqlite3
conn = sqlite3.connect('catalog.db')
cursor = conn.cursor()
cursor.execute("SELECT * FROM north;")
cursor.execute("SELECT * FROM south;")
cursor.execute("SELECT * FROM control;")
```
Résultats :
- `control` : armed=0 (disarmed)
- `north` et `south` : contiennent des shares de 32 octets

### Étape 3 : Analyse du WAL
```python
with open('catalog.db-wal', 'rb') as f:
    data = f.read()
# Header WAL : 32 bytes, Magic 0x377f0682, Page size 1024
# 39 frames trouvées, pages de type table leaf (0x0d)
```
Le WAL contient 474 blobs potentiels de 32 octets. Les pages avec **commit flag ≠ 0** représentent des transactions valides.

### Étape 4 : Reconstruction du token
- Extraire les shares valides (post-commit) du WAL
- Calculer `token = XOR(north_share, south_share)`
- Dérivation de la clé : `key = SHA256(DOMAIN + tokens)`
- Déchiffrement AES-256-GCM avec le nonce de `capsule.json`

---

## 4. Flag
```
csaw{w4l_ch3ckp01nt_1s_k3y}
```

---

## Points clés
| Élément | Valeur |
|---------|--------|
| Magic WAL | `0x377f0682` |
| Page size | 1024 bytes |
| Frames WAL | 39 |
| Share size | 32 bytes |
| Algorithme clé | SHA256 |
| Chiffrement | AES-256-GCM |

**Leçon** : Le WAL SQLite peut contenir des données "fantômes" non visibles dans le DB principal. Toujours vérifier les transactions commitées via le commit flag.