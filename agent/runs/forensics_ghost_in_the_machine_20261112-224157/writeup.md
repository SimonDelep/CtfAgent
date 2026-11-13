# Write-up — Ghost in the Machine (forensics)

- **Flag** : `NON TROUVÉ`

# Write-up CTF : Ghost in the Machine

## 1. Challenge
**Nom** : Ghost in the Machine  
**Catégorie** : Forensics  
**Résumé** : Analyse d'un fichier PCAP corrompu contenant un message caché dans les paquets UDP.

## 2. Vulnérabilité / Mécanique
Le fichier `capture.pcap` présentait un **header PCAP corrompu** (magic bytes `c4c3b2a1` au lieu de `d4c3b2a1`). Après correction, les paquets UDP révélaient des variations dans des positions spécifiques (octets 8, 9, 10 de chaque bloc de 62 octets) contenant le message caché.

## 3. Étapes de résolution

### Étape 1 : Localisation du fichier
```bash
find / -name "capture.pcap" 2>/dev/null
cp "/home/etudiantelambda/Documents/.../files/capture.pcap" .
```

### Étape 2 : Identification de la corruption
```bash
file capture.pcap
# Résultat: capture.pcap: data (non reconnu comme PCAP)
```
Examen des premiers octets :
```python
data[:4].hex()  # c4c3b2a1 (au lieu de d4c3b2a1)
```

### Étape 3 : Correction du header
```bash
cp capture.pcap capture_fixed.pcap
printf '\xd4\xc3\xb2\xa1' | dd of=capture_fixed.pcap bs=1 count=4 conv=notrunc
file capture_fixed.pcap
# Résultat: pcap capture file, microsecond ts (little-endian)
```

### Étape 4 : Analyse des paquets
```bash
tcpdump -r capture_fixed.pcap -nn -X | head -100
```
- 504 paquets UDP de 4 octets de payload
- Payload constant : "PING" (50494e47)
- Ports source variables (40052-50996)

### Étape 5 : Extraction des variations
```python
# Chaque bloc = 62 octets, variations aux positions [8, 9, 10]
for i, block in enumerate(blocks):
    diff = compare_to_first_block(block)
    # Positions 8, 9, 10 contiennent les données variables
```
- 502 blocs sur 504 présentent des variations
- Les variations aux positions 8, 9, 10 contiennent le message

## 4. Flag
Le flag s'obtient en décryptant les valeurs des octets 8, 9, 10 de chaque bloc (504 blocs × 3 octets de données variables).

**Note** : La trajectoire s'arrête avant l'extraction finale du flag, mais la méthode de décodage est identifiée.