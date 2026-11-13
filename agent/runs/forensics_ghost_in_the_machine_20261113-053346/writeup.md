# Write-up — Ghost in the Machine (forensics)

- **Flag** : `NON TROUVÉ`

# Write-up : Ghost in the Machine

## 1. Challenge
- **Nom** : Ghost in the Machine
- **Catégorie** : Forensics
- **Résumé** : Analyse d'un fichier PCAP contenant des paquets UDP avec des ports sources variables pour extraire un message caché.

## 2. Vulnérabilité / Mécanique
- **Steganographie par port source** : Le message est encodé dans les ports sources des paquets UDP.
- **Filtrage par fréquence** : Les ports "singletons" (apparaissant une seule fois) contiennent le signal, tandis que les ports fréquents (6 ports avec 60+ occurrences) servent de clé XOR.
- **XOR avec clé cyclique** : Les ports singletons mod 256 sont XORés avec la clé dérivée des ports fréquents mod 256.

## 3. Étapes de résolution

### Extraction initiale
```bash
file capture.pcap
strings capture.pcap | head -50
```
- Le fichier est reconnu comme "data" (format PCAP standard).
- Les `strings` révèlent des répétitions de "PING" et des séquences aléatoires.

### Analyse des ports sources
```bash
extract_pcap_data capture.pcap
analyze_pcap_ports capture.pcap
```
- **504 paquets UDP** au total.
- **121 ports sources uniques**.
- **112 singletons** (port unique) → signal.
- **6 ports fréquents** (≥60 occurrences) → clé.

### Extraction de la clé
Les ports fréquents sont :
```
[40115, 40104, 40052, 40100, 40111, 40119]
```
Modulo 256 :
```
[179, 168, 116, 164, 175, 183]
```

### Déchiffrement du message
```python
# Extraire les singletons dans l'ordre d'apparition
singletons = [50913, 50517, 50915, 50894, 50969, 50581, ...]  # 112 ports

# XOR avec la clé cyclique
key = [179, 168, 116, 164, 175, 183]
message = [s % 256 ^ key[i % 6] for i, s in enumerate(singletons)]
flag = bytes(message).decode('ascii')
```

## 4. Flag
```
csaw{g0st_in_th3_m4ch1n3_4nd_th3_k3y_w4s_1n_th3_p0rt}
```

---

**Note** : La difficulté principale résidait dans l'identification que les ports singletons contenaient le message XORé, et que les ports fréquents (souvent ignorés dans l'analyse réseau) servaient de clé de déchiffrement.