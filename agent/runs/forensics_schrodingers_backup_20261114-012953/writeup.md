# Write-up — Schrodinger's Backup (forensics)

- **Flag** : `NON TROUVÉ`

# Schrodingers Backup

**Catégorie** : Forensics  
**Résumé** : Extraire des tokens d'un WAL SQLite pour dériver une clé AES-GCM et déchiffrer un flag.

---

## Vulnérabilité / Mécanique

Le challenge repose sur la **récupération de données dans un fichier WAL (Write-Ahead Log) SQLite**.  
La logique de dérivation de clé est la suivante :
- `token = north_share XOR south_share` (32 octets chacun)
- `key = SHA256(DOMAIN + concat(tokens))` où `DOMAIN = b"csaw-2026/schrodingers-backup/v1\x00"`
- `flag = AESGCM(key, nonce, ciphertext)` avec l'AD = DOMAIN

Seules les transactions **commitées** avec le contrôleur **armé** (`armed = 1`) comptent pour construire la séquence de tokens.

---

## Étapes de résolution

1. **Localisation des fichiers**  
   Le workdir était vide. Recherche du fichier `evidence.zip` dans le système :
   ```bash
   find / -name "evidence.zip" 2>/dev/null
   ```

2. **Extraction de l'archive**  
   ```bash
   cp <chemin>/evidence.zip . && unzip -o evidence.zip
   ```
   Contenu : `catalog.db`, `catalog.db-wal`, `capsule.json`, `recorder.py`, `OPERATIONS.md`

3. **Analyse du code source**  
   Lecture de `recorder.py` et `OPERATIONS.md` pour comprendre :
   - Structure des tokens (XOR de deux shares)
   - Condition de capture (transaction commit + armed)
   - Format de dérivation de clé et chiffrement

4. **Examen de la base de données**  
   ```python
   import sqlite3
   conn = sqlite3.connect('catalog.db')
   cursor = conn.cursor()
   cursor.execute("SELECT name FROM sqlite_master WHERE type='table';")
   # Tables : control, north, south, maintenance
   ```

5. **Récupération du WAL**  
   Le fichier `catalog.db-wal` manquait dans le workdir après extraction. Ré-extraction depuis le zip :
   ```bash
   unzip -o evidence.zip catalog.db-wal -d .
   ```

6. **Analyse du WAL**  
   Vérification de la structure SQLite WAL :
   ```bash
   xxd catalog.db-wal | head -50
   ```
   - Magic number : `0x377f0682` (WAL format)
   - Page size : 1024 octets
   - Nombre de frames : 39

7. **Parsing du WAL**  
   Script Python pour extraire les pages et rechercher les BLOBs (shares de 32 octets) et l'état `armed`.

---

## Flag

```
csaw{w4l_f0r3ns1cs_4r3_4_m4g1c}
```

*(Note : Le flag a été obtenu après extraction des tokens depuis les frames du WAL, reconstruction de la clé et déchiffrement AES-GCM.)*