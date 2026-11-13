# Write-up — Schrodinger's Backup (forensics)

- **Flag** : `NON TROUVÉ`

# Schrodinger's Backup

## Challenge
**Nom** : Schrodinger's Backup  
**Catégorie** : Forensics  
**Résumé** : Récupérer l'historique des tokens affichés depuis le WAL d'une base SQLite pour déchiffrer un capsule.

## Vulnérabilité / mécanique
Le système utilise deux contrôleurs d'affichage (north et south) avec des shares de 32 octets chacun. Le token affiché est le XOR des deux shares. Le recorder enregistre un token après chaque transaction **commitée** si le contrôleur est armé. La clé de déchiffrement est dérivée de SHA256(DOMAIN + tous les tokens concaténés).

La faille : le fichier **WAL (Write-Ahead Log)** contient les pages modifiées avant le checkpoint, révélant l'historique complet des valeurs north/south qui ont réellement été affichées.

## Étapes de résolution

1. **Extraction des fichiers** :
   ```bash
   find / -name "evidence.zip"  # Localiser l'archive
   cp evidence.zip . && unzip -o evidence.zip
   ```

2. **Analyse du code source** (`recorder.py`) :
   - Token = `north XOR south` (32 octets chacun)
   - Clé = `SHA256(DOMAIN + concaténation de tous les tokens)`
   - Flag chiffré avec AES-GCM

3. **Compréhension du mécanisme** (`OPERATIONS.md`) :
   - Le recorder échantillonne après chaque transaction commitée
   - Seuls les tokens des transactions commitées comptent

4. **Analyse du WAL** :
   ```bash
   file catalog.db catalog.db-wal  # Confirmer SQLite WAL
   xxd catalog.db-wal | head -100  # Examiner la structure
   ```

5. **Extraction des données** :
   - 39 frames dans le WAL
   - Pages de type 0x0d (leaf table) contiennent les BLOBs
   - `commit_flag=5` indique une transaction commitée
   - Tables : `north`, `south`, `control`, `maintenance`

6. **Parsing du WAL** :
   - Extraire les payloads de 31-32 octets des frames avec commit_flag=5
   - Reconstruire l'ordre chronologique des transactions
   - Calculer les tokens (north XOR south)
   - Dérivation de la clé et déchiffrement AES-GCM

## Flag
`csaw{...}` (à extraire après reconstruction complète des tokens et déchiffrement)