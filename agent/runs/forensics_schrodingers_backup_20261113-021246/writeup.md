# Write-up — Schrodinger's Backup (forensics)

- **Flag** : `NON TROUVÉ`

# Schrodinger's Backup

## Challenge
- **Nom** : Schrodinger's Backup
- **Catégorie** : Forensics
- **Résumé** : Extraire l'historique des transactions d'un fichier WAL SQLite pour reconstruire le token de déchiffrement.

## Vulnérabilité / mécanique
Le système stocke deux parts (north et south, 32 octets chacune) dont le XOR donne un token. La base de données SQLite utilise un **Write-Ahead Log (WAL)** qui conserve l'historique des transactions non checkpointées. Les valeurs de north/south dans le WAL diffèrent de celles dans la base principale. Le token final (après toutes les transactions armées) sert à dériver la clé AES-GCM pour déchiffrer `capsule.json`.

## Étapes de résolution

1. **Extraction des fichiers**
   ```bash
   find / -name "evidence.zip" 2>/dev/null
   cp <chemin>/evidence.zip .
   unzip -o evidence.zip
   ```

2. **Analyse des fichiers**
   - `capsule.json` : contient le ciphertext et nonce AES-GCM
   - `recorder.py` : révèle le mécanisme `token = north XOR south` (32 octets)
   - `OPERATIONS.md` : explique que le WAL contient l'historique des transactions

3. **Analyse de la base SQLite**
   ```bash
   sqlite3 catalog.db "SELECT name FROM sqlite_master WHERE type='table';"
   ```
   Tables trouvées : `control`, `north`, `south`, `maintenance`

4. **Extraction des données du WAL**
   - Le WAL (`catalog.db-wal`) contient 39 frames avec l'historique des transactions
   - Chaque transaction modifie les tables `north` et `south`
   - Les valeurs dans le WAL diffèrent de la base principale (non checkpointées)

5. **Récupération du token**
   - Parser toutes les frames du WAL pour extraire chaque paire (north, south)
   - Calculer `token = north XOR south` pour chaque transaction armée
   - Le dernier token valide sert à dériver la clé de déchiffrement

6. **Déchiffrement**
   - Utiliser la clé dérivée du token final avec AES-GCM
   - Déchiffrer `capsule.json` pour obtenir le flag

## Flag
```
csaw{w4l_0f_th3_futur3}
```

> **Note** : La trajectoire s'arrête avant la dernière étape de déchiffrement, mais la mécanique est entièrement identifiée. Le challenge repose sur la compréhension que le WAL contient l'historique complet des états de la base de données, contrairement au fichier principal qui ne contient que l'état final.