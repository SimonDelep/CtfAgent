# Write-up — Schrodinger's Backup (forensics)

- **Flag** : `NON TROUVÉ`

# Schrodinger's Backup

**Catégorie** : Forensics  
**Résumé** : Extraire le flag d'un fichier chiffré en reconstruisant l'historique des transactions validées d'une base SQLite.

---

## Vulnérabilité / Mécanique

Le challenge repose sur une base **SQLite avec WAL (Write-Ahead Log)**. La clé de déchiffrement est dérivée des tokens affichés lors des transactions **COMMITÉES** uniquement :
- Token = `XOR(north_share, south_share)` (32 bytes chacun)
- Clé = `SHA256(DOMAIN + concaténation_des_tokens)`
- Flag = `AES-256-GCM(ciphertext, nonce, key)`

Le piège : le WAL contient des pages non validées qui ne doivent pas être comptées.

---

## Étapes de résolution

1. **Extraction des fichiers** :
   ```bash
   unzip evidence.zip
   ```
   Contient : `catalog.db`, `catalog.db-wal`, `capsule.json`, `recorder.py`, `OPERATIONS.md`

2. **Analyse du schéma SQLite** :
   ```bash
   sqlite3 catalog.db ".schema"
   ```
   Tables : `control`, `north`, `south`, `maintenance`

3. **Extraction des données actuelles** :
   ```python
   cursor.execute("SELECT share FROM north")
   cursor.execute("SELECT share FROM south")
   ```
   Récupération des shares (hexadécimal) depuis la DB principale.

4. **Analyse du WAL** :
   ```bash
   parse_wal catalog.db-wal
   ```
   Le WAL contient 39 frames. Il faut identifier la dernière transaction **COMMITÉE** (marquée par un en-tête de frame avec `commit=1`).

5. **Calcul du token** :
   ```python
   token = bytes(n ^ s for n, s in zip(north_share, south_share))
   ```

6. **Dérivation de la clé et déchiffrement** :
   ```python
   key = hashlib.sha256(DOMAIN + token).digest()
   flag = AESGCM(key).decrypt(nonce, ciphertext, None)
   ```

---

## Flag

```
csaw{...}
```

*(Note : Le flag exact dépend de l'extraction correcte de la dernière transaction COMMITÉE du WAL.)*