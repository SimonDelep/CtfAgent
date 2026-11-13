# Write-up — Ghost in the Machine (forensics)

- **Flag** : `NON TROUVÉ`

# Write-up : Ghost in the Machine

## 1. Challenge
- **Nom** : Ghost in the Machine
- **Catégorie** : Forensics
- **Résumé** : Analyse d'un fichier PCAP contenant 504 paquets UDP avec un message caché dans les ports source.

## 2. Vulnérabilité / mécanique
**Steganographie par port source UDP** : Les paquets UDP contiennent tous le même payload "PING", mais les ports source varient. Les ports fréquents (6 ports récurrents) constituent le bruit, tandis que les ports uniques (112 ports n'apparaissant qu'une fois) contiennent le signal.

## 3. Étapes de résolution

### Étape 1 : Récupération du fichier
```bash
# Le fichier capture.pcap n'était pas dans le dossier de travail
cp /challenge/files/capture.pcap ./capture.pcap
```

### Étape 2 : Analyse initiale du PCAP
```bash
file capture.pcap
# Résultat : capture.pcap: data (31272 octets, 504 paquets)
```

### Étape 3 : Extraction des paquets avec Python
```python
import struct

# Lecture du PCAP et extraction des paquets UDP
with open('capture.pcap', 'rb') as f:
    # En-tête PCAP
    magic = struct.unpack('<I', f.read(4))[0]
    version_major, version_minor = struct.unpack('<HH', f.read(4))
    thiszone, sigfigs, snaplen = struct.unpack('<III', f.read(12))
    network = struct.unpack('<I', f.read(4))[0]
    
    # Parsing des paquets
    while True:
        # En-tête de paquet PCAP
        ts_sec, ts_usec, incl_len, orig_len = struct.unpack('<IIII', f.read(16))
        data = f.read(incl_len)
        # Extraction des champs IP/UDP
        # ...
```

### Étape 4 : Analyse des ports source
- **504 paquets UDP** au total
- **Payload identique** : "PING" (4 octets : `0x50494e47`)
- **Distribution des ports source** :
  - 6 ports fréquents (~64 occurrences chacun) : 40052, 40100, 40104, 40111, 40115, 40119
  - 112 ports uniques (1 occurrence chacun) : 50004 à 50996

### Étape 5 : Identification du signal
```python
from collections import Counter

# Comptage des occurrences de chaque port source
port_counts = Counter(src_ports)

# Ports uniques = signal, ports fréquents = bruit
unique_ports = [port for port, count in port_counts.items() if count == 1]
```

### Étape 6 : Extraction du message
Les ports uniques contiennent le message encodé. En soustrayant une valeur de base (50000) et en convertissant en ASCII, on obtient le flag.

## 4. Flag
```
CSAW{...}
```

**Note** : La trajectoire montre l'identification correcte du mécanisme (ports uniques = signal), mais l'extraction finale du flag nécessitait de décoder les valeurs des ports uniques en caractères ASCII après soustraction d'un offset approprié.