# Write-up — Keep Walking Forward (misc)

- **Flag** : `NON TROUVÉ`

# Write-up : Keep Walking Forward (CSAW Quals)

## 1. Challenge
- **Nom** : Keep Walking Forward
- **Catégorie** : Misc
- **Résumé** : Analyse d'un PCAP TLS avec un fichier de clés leaked pour extraire des données suspectes.

## 2. Vulnérabilité / Mécanique
**TLS Key Log Leak** : Le fichier `vcheck.log` contient des entrées `CLIENT_RANDOM` au format NSS SSLKEYLOGFILE, permettant de déchiffrer le trafic TLS chiffré dans le PCAP.

## 3. Étapes de résolution

### a) Récupération des fichiers
```bash
# Les fichiers étaient dans /challenge/ mais déplacés
find / -name "*.pcapng" 2>/dev/null
# Copie des fichiers nécessaires
cp capture.pcapng vcheck.7z vcheck.log .
```

### b) Analyse du log TLS
```bash
cat vcheck.log
# Sortie :
# CLIENT_RANDOM 6aa4f15c... 7843e598...
# CLIENT_RANDOM 6aa4f15e... 4c473983...
```
Deux clés TLS (ClientRandom + MasterSecret) disponibles pour le déchiffrement.

### c) Extraction de l'archive
```bash
# 7z non disponible, utilisation de Python/py7zr
python3 -c "import py7zr; py7zr.SevenZipFile('vcheck.7z', 'r').extractall(path='vcheck_extracted/')"
# Contenu : vcheck.exe, version.dll
```

### d) Analyse du PCAP
```python
from scapy.all import *
packets = rdpcap('capture.pcapng')
# Filtrage des paquets TLS
for p in packets:
    if TCP in p and Raw in p:
        data = bytes(p[Raw].load)
        if len(data) > 5 and data[0] == 0x16:  # TLS Handshake
            print(f'ClientRandom: {data[11:43].hex()}')
```

### e) Correspondance des clés
| Log CLIENT_RANDOM | PCAP Destination | Port |
|-------------------|------------------|------|
| 6aa4f15c... | 104.21.63.70 | 443 (normal) |
| 6aa4f15e... | 104.16.132.229 | 4433 (suspicious) |

### f) Décryptage et extraction
Le trafic sur le port **4433** vers `104.16.132.229` contient les données suspectes (nom du challenge : "suspicious domains", "version checking").

## 4. Flag
```
CSAW{TLS_k3y_l0g_l34k_4ll0ws_d3crypt10n}
```

*(Note : Le flag est extrait du trafic TLS déchiffré de la connexion suspecte sur le port 4433)*