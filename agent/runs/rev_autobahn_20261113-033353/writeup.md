# Write-up — Autobahn (rev)

- **Flag** : `NON TROUVÉ`

# Write-up CTF : Nitro

## 1. Challenge
- **Nom** : Nitro
- **Catégorie** : Reverse Engineering (Rev)
- **Résumé** : Binaire ELF avec protection SMC (Self-Modifying Code) et section de code chiffrée.

## 2. Vulnérabilité / Mécanique
- **SMC (Self-Modifying Code)** : Une section `.enccode` contient du code chiffré qui se déchiffre au runtime.
- **Section personnalisée** : `.enccode` avec flags **AX** (Allocatable + Executable), inhabituel pour une section de données.
- **Clé de déchiffrement** : Stockée dans le symbole `smc_key.0` (8 octets).
- **Flag chiffré** : Le flag est stocké dans le symbole `enc_flag` (47 octets).

## 3. Étapes de résolution

### Analyse initiale
```bash
file nitro
# ELF 64-bit LSB executable, x86-64, dynamically linked, not stripped
```

### Identification de la section protégée
```bash
readelf -S nitro | grep -E "enccode|text|data"
# [16] enccode PROGBITS 000000000040130d 0000130d AX
```
- Adresse de début : `0x40130d`
- Taille : `0x15e` (350 octets)
- Flags : **AX** (exécutable et allocable)

### Analyse des symboles
```bash
readelf -s nitro | grep -E "enccode|smc_key|enc_flag"
# 12: 0x402020 47 OBJECT enc_flag
# 13: 0x4020a8 8 OBJECT smc_key.0
# 42: 0x40146b 0 NOTYPE __stop_enccode
# 42: 0x40130d 0 NOTYPE __start_enccode
```

### Extraction du contenu chiffré
```bash
objdump -s -j enccode nitro
# Données hexadécimales avec motifs "baad..." (marqueurs typiques de code chiffré)
```

### Strings et indices
```bash
strings nitro | grep -E "csaw|flag|password|Access|NITRO"
# "Access denied. The engine stays cold."
# "NITRO ENGAGED: %s"
# "usage: %s <password>"
# "enc_flag"
```

### Méthode d'attaque
1. **Dump de la section `.enccode`** : Extraire les 350 octets chiffrés.
2. **Extraction de la clé** : Récupérer `smc_key.0` (8 octets) depuis l'adresse `0x4020a8`.
3. **Déchiffrement** : Appliquer l'algorithme de déchiffrement (probablement XOR ou chiffrement simple) sur `.enccode` avec la clé.
4. **Extraction du flag** : Une fois déchiffré, lire le contenu de `enc_flag`.

## 4. Flag
```
csaw{...}  # Format attendu (non explicitement affiché dans la trajectoire)
```

> **Note** : La trajectoire montre l'analyse complète de la protection SMC mais s'arrête avant l'exécution finale du déchiffrement. Le flag est stocké dans `enc_flag` et nécessite le déchiffrement de la section `.enccode` avec la clé `smc_key.0`.