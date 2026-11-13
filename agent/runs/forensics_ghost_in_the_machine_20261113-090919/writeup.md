# Write-up — Ghost in the Machine (forensics)

- **Flag** : `NON TROUVÉ`

# Ghost in the Machine

## Challenge
- **Nom** : Ghost in the Machine
- **Catégorie** : Forensics
- **Résumé** : Analyser un fichier PCAP pour extraire un message caché dans les ports sources UDP.

## Vulnérabilité / mécanique
- **Steganographie par port source** : Les ports sources des paquets UDP contiennent le message codé
- **Filtrage par fréquence** : Les ports fréquents (64+ occurrences) sont du bruit, seuls les singletons (1 occurrence) contiennent le signal
- **Format PCAP modifié** : Magic number inversé (`c4c3 b2a1` au lieu de `a1b2 c3d4`) nécessitant un parsing manuel

## Étapes de résolution

### 1. Localisation du fichier
```bash
find / -name "capture.pcap" 2>/dev/null
```
Le fichier n'était pas dans le dossier attendu, il a été copié dans le workdir.

### 2. Analyse initiale
```bash
file capture.pcap
```
Résultat : `capture.pcap: data` (format non standard)

### 3. Analyse des ports
```bash
analyze_pcap_ports capture.pcap
```
- **504 paquets** totaux
- **121 ports sources uniques**
- **112 singletons** (ports apparaissant 1 fois)
- **6 ports fréquents** (~64 occurrences chacun : 40115, 40104, 40052, 40100, 40111, 40119)

### 4. Examen du contenu
```bash
xxd capture.pcap | head -5
```
- Magic number : `c4c3 b2a1` (byte order inversé)
- Payload UDP : toujours `PING` (0x50494e47)
- Le signal est donc dans les **ports sources**

### 5. Parsing manuel du PCAP
```bash
python3 -c "
import struct
with open('capture.pcap', 'rb') as f:
    data = f.read()
# Header PCAP avec byte order little-endian
magic, version_major, version_minor, thiszone, sigfigs, snaplen, network = struct.unpack('<IHHIIII', data[:24])
# Extraction des paquets UDP et ports sources
"
```

### 6. Extraction des singletons
Les 112 ports singletons ont été extraits dans l'ordre chronologique :
```
[50913, 50517, 50915, 50894, 50969, 50581, 50957, 50698, 50142, 50207, ...]
```

### 7. Tentatives de décodage
Différents offsets testés :
- `port % 256` → non lisible
- `port - 0xc300` → non lisible
- `port - 0xc400` → non lisible

Le hint indiquait : *"the sender left the key hiding in plain sight, in another column you skipped"*

## Flag
Le flag n'a pas été complètement extrait dans la trajectoire visible, mais la méthodologie était établie :
- **Format attendu** : `csaw{...}`
- **Méthode** : Décoder les 112 ports singletons dans l'ordre chronologique avec l'offset correct
- **Indice** : L'offset de décodage se trouve dans les ports fréquents (la "clé" est cachée dans les ports 40115, 40104, etc.)

**Note** : La trajectoire s'arrête pendant l'extraction des données. Le flag final nécessiterait d'appliquer l'offset correct (probablement basé sur les ports fréquents) aux ports singletons pour obtenir les caractères ASCII du message.