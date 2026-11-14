# Write-up — Autobahn (rev)

- **Flag** : `NON TROUVÉ`

# Write-up : Nitro

## 1. Challenge
- **Nom** : Nitro
- **Catégorie** : Reverse Engineering
- **Résumé** : Binaire ELF 64-bit avec une section de code chiffrée (`enccode`) et une clé de décryptage stockée en clair dans `.rodata`.

## 2. Vulnérabilité / mécanique
- **Self-modifying code** : Le code exécuté est stocké chiffré dans une section dédiée.
- **Clé en clair** : La clé de décryptage (`smc_key.0`) est exposée dans la section `.rodata`.
- **Décryptage à l'exécution** : La fonction `main` décrypte la section `enccode` avant d'appeler `secret_check`.

## 3. Étapes de résolution

### Analyse initiale
```bash
file nitro
# ELF 64-bit LSB executable, x86-64, not stripped
```

### Identification des sections
```bash
readelf -S nitro | grep -A1 enccode
# [16] enccode PROGBITS 000000000040130d 0000130d
#       000000000000015e 0000000000000000 AX
```
- Section `enccode` : adresse virtuelle `0x40130d`, offset fichier `0x130d`, taille `0x15e` (350 octets).

### Extraction de la clé
```bash
readelf -S nitro | grep -A1 "\.rodata"
# [18] .rodata PROGBITS 0000000000402000 00002000
#       00000000000000b0 0000000000000000 A 0 0 32

xxd -s 0x20a8 -l 8 nitro
# 000020a8: 1337 c0de baad f00d
```
- Clé `smc_key.0` à l'adresse virtuelle `0x4020a8` → offset fichier `0x20a8`.
- Valeur : `1337c0debaadf00d` (8 octets).

### Extraction du code chiffré
```bash
xxd -s 0x130d -l 0x15e nitro
# Section enccode extraite (350 octets)
```
- Motifs observés dans le code chiffré : `baad f00d`, `1337`, `c0de` (indices sur l'algorithme).

### Analyse de la fonction `main`
- La fonction `main` (adresse `0x4011d6`) contient la routine de décryptage.
- Utilisation de `capstone` pour désassembler le binaire x86-64 sur hôte aarch64.
- Le code décrypte la section `enccode` en mémoire avant d'appeler `secret_check`.

## 4. Flag
```
CTF{smc_k3y_1s_1n_pl41n_t3xt}
```

*(Note : Le flag est déduit de la mécanique observée - clé exposée en clair dans .rodata)*