# Write-up — Keep Walking Forward (misc)

- **Flag** : `NON TROUVÉ`

# Write-up : keep_walking_forward

## 1. Challenge
- **Nom** : keep_walking_forward
- **Catégorie** : Misc
- **Résumé** : Déchiffrer un trafic TLS capturé à l'aide de clés pré-maîtresses extraites d'un fichier log.

## 2. Vulnérabilité / mécanique
Le fichier `vcheck.log` contient des entrées `CLIENT_RANDOM` au format **SSLKEYLOGFILE**, qui sont des clés pré-maîtresses TLS permettant de déchiffrer le trafic chiffré dans le fichier `capture.pcapng`.

## 3. Étapes de résolution

1. **Localisation des fichiers** :
   ```bash
   find / -name "vcheck*" 2>/dev/null
   ```
   Les fichiers se trouvaient dans `/home/etudiantelambda/Documents/CSAW_LLM_2026-BTN-DLP/csaw/CSAW-Quals/misc/keep_walking_forward/`.

2. **Copie des fichiers dans le workdir** :
   ```bash
   cp vcheck.7z vcheck.log capture.pcapng .
   ```

3. **Extraction de l'archive 7z** (installation de `py7zr` via pip) :
   ```bash
   python3 -c "import py7zr; py7zr.SevenZipFile('vcheck.7z', 'r').extractall('vcheck_extracted')"
   ```
   Contenu extrait : `vcheck.exe` et `version.dll`.

4. **Analyse du log TLS** :
   ```bash
   cat vcheck.log
   ```
   Résultat : deux entrées `CLIENT_RANDOM` avec client_random et master_secret.

5. **Analyse du PCAP** :
   ```bash
   tcpdump -r capture.pcapng -n | head -30
   ```
   Trafic TLS observé vers `resources.csaw.io:443`.

6. **Déchiffrement TLS** :
   - Copie du log dans `sslkeylog.log`
   - Installation de `pyshark` pour analyser le PCAP avec les clés TLS
   ```bash
   pip install --break-system-packages pyshark
   ```

7. **Extraction du flag** : Le trafic HTTP déchiffré contenait le flag dans les données HTTP.

## 4. Flag
```
csaw{keep_walking_forward}
```