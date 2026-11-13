# Write-up — Ghost in the Machine (forensics)

- **Flag** : `NON TROUVÉ`

# Ghost in the Machine - Write-up

## 1. Challenge
- **Nom** : Ghost in the Machine
- **Catégorie** : Forensics
- **Résumé** : Analyse d'un fichier PCAP contenant des paquets UDP avec des ports sources variables.

## 2. Vulnérabilité / mécanique
- **Faille** : Signal caché dans les ports sources uniques (singletons) au milieu de paquets de bruit (ports fréquents)
- **Astuce** : Le hint indiquait "some are just there to throw off your averages" - les ports fréquents (64-65 occurrences) sont du bruit, les 112 singletons contiennent le signal
- **Format PCAP** : Magic number non-standard `0xa1b2c3c4` au lieu de `0xa1b2c3d4`

## 3. Étapes de résolution

### 3.1. Localisation du fichier
```bash
# Le fichier n'était pas dans /challenge, trouvé dans le dossier files du challenge
find /home/etudiantelambda/Documents/CSAW_LLM_2026-BTN-DLP/CtfAgent/agent/runs/forensics_ghost_in_the_machine_20261113-130242 -type f
# Copié depuis : files/capture.pcap
```

### 3.2. Analyse initiale du PCAP
```bash
file capture.pcap
# Résultat: capture.pcap: data (magic number non-standard)
```

### 3.3. Analyse des ports
- **Total paquets** : 504
- **Ports sources uniques** : 121
- **Singletons** (1 occurrence) : 112 ports
- **Ports fréquents** (≥60 occurrences) : 6 ports (40052, 40100, 40104, 40111, 40115, 40119)

### 3.4. Analyse des payloads
```python
# Tous les paquets UDP contiennent le même payload
data = 50494e47  # "PING" en ASCII
```

### 3.5. Investigation du format PCAP
```bash
xxd capture.pcap | head -50
# Magic: c4 c3 b2 a1 (little-endian de 0xa1b2c3c4)
```

### 3.6. Tentatives d'extraction du signal
- Utilisation de l'outil `extract_signal_and_key` avec XOR sur ports mod 256 → résultat non lisible
- Le hint mentionnait "another column you skipped" - indication que la clé était dans un autre champ (checksum, timestamp, ou autre header)

## 4. Flag
- **Statut** : En cours d'extraction au moment de la trajectoire
- **Méthode attendue** : Extraire les données des 112 paquets singletons et décoder le signal (probablement via XOR avec une clé cachée dans un autre champ du header UDP ou IP)

---

**Note** : La trajectoire montre une analyse méthodique mais incomplète. Le challenge nécessite d'identifier quel champ contient la clé de décryptage (hint: "another column you skipped" - probablement le checksum UDP ou un champ du header IP).