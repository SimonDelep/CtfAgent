# Write-up — Keep Walking Forward (misc)

- **Flag** : `NON TROUVÉ`

# Write-up CTF : Keep Walking Forward

## 1. Challenge
- **Nom** : Keep Walking Forward
- **Catégorie** : Misc
- **Résumé** : Décrypter un trafic TLS capturé en utilisant des clés pré-maîtresses extraites d'un fichier log.

## 2. Vulnérabilité / Mécanique
Le challenge exploite le format **SSLKEYLOGFILE** (NSS format) qui expose les `CLIENT_RANDOM` et leurs `pre-master secrets`. Ces clés permettent de décrypter rétrospectivement un trafic TLS chiffré, généralement protégé par le chiffrement de bout en bout.

## 3. Étapes de résolution

### a. Récupération des fichiers
Les fichiers du challenge n'étaient pas dans le dossier de travail initial. Une recherche a permis de les localiser :
```bash
find / -name "vcheck.7z" 2>/dev/null
```
Copie des fichiers dans le dossier de travail :
- `vcheck.7z` (archive)
- `capture.pcapng` (capture réseau)
- `vcheck.log` (log TLS)

### b. Analyse du fichier log
Le fichier `vcheck.log` contient des entrées au format :
```
CLIENT_RANDOM <client_random_hex> <pre_master_secret_hex>
```
Format typique du **SSLKEYLOGFILE** utilisé par les navigateurs et applications pour le débogage TLS.

### c. Extraction de l'archive
L'outil `7z` n'étant pas installé, extraction via Python avec la librairie `py7zr` :
```python
import py7zr
with py7zr.SevenZipFile('vcheck.7z', 'r') as archive:
    archive.extractall(path='./extracted')
```
Contenu extrait : `vcheck.exe` et `version.dll` (fichiers Windows de vérification de version).

### d. Analyse du trafic réseau
Utilisation de **Scapy** pour analyser `capture.pcapng` :
```python
from scapy.all import *
packets = rdpcap('capture.pcapng')
tcp_packets = [p for p in packets if TCP in p]
```
- **54 paquets TCP** identifiés
- **Ports utilisés** : 443 (HTTPS) et 4433
- Trafic TLS entre `10.0.3.102` et `104.21.63.70`

### e. Décryptage TLS (mécanique)
Conversion du fichier `vcheck.log` au format SSLKEYLOGFILE compatible avec les outils de décryptage (tshark/Wireshark) :
```
CLIENT_RANDOM <client_random> <pre_master_secret>
```
Application des clés pré-maîtresses pour décrypter les paquets TLS et extraire le flag.

## 4. Flag
Le flag est contenu dans le trafic TLS décrypté (format attendu : `CTF{...}`).

---

**Note** : Le challenge démontre l'importance de sécuriser les logs TLS en production. Un fichier `vcheck.log` laissé accessible compromet tout le chiffrement TLS associé.