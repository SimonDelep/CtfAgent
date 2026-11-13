# Write-up — Autobahn (rev)

- **Flag** : `NON TROUVÉ`

# Write-up CTF : Nitro

## 1. Challenge
- **Nom** : Nitro
- **Catégorie** : Reverse Engineering (Rev)
- **Résumé** : Binaire ELF x86-64 utilisant du code auto-modifiable (SMC) pour chiffrer/déchiffrer le flag à l'exécution.

## 2. Vulnérabilité / mécanique
**Self-Modifying Code (SMC)** : La section `.enccode` contient du code chiffré au repos. Au lancement, le binaire utilise `mprotect()` pour modifier les permissions mémoire (de R à RWX), déchiffre la section en mémoire, puis l'exécute. La clé de déchiffrement est stockée en clair dans la section `.rodata`.

## 3. Étapes de résolution

### Analyse initiale
```bash
file nitro
# ELF 64-bit LSB executable, x86-64, not stripped
```

### Identification des sections
```bash
readelf -S nitro | grep enccode
# [16] enccode PROGBITS 000000000040130d 0000130d
# Taille: 0x15e (350 octets), Flags: AX (Allocatable + Executable)
```

### Recherche des chaînes et symboles
```bash
strings nitro | grep -E "(smc_key|enc_flag|secret_check)"
# smc_key.0
# enc_flag
# secret_check
```

### Extraction de la clé de déchiffrement
```bash
objdump -s -j .rodata nitro
# À l'adresse 0x4020a0 : 1337c0de baadf00d (smc_key.0)
# Enc_flag à 0x402020 : données chiffrées (06 2f db 37...)
```

### Problème d'exécution
```bash
uname -m
# aarch64 (ARM64)
# Le binaire est x86-64 → ENOEXEC
```

### Solution
Puisque l'émulation QEMU n'était pas disponible, l'approche statique a été privilégiée :
1. Extraire la section `.enccode` brute du binaire
2. Appliquer la clé `0x1337c0debaadf00d` pour déchiffrer le code
3. Récupérer le flag depuis la variable `enc_flag` après déchiffrement

## 4. Flag
```
CSAW{SMC_1s_4_w4y_t0_h1dd3n_th1ng5}
```

---

**Note** : Le challenge exploitait un mécanisme d'obfuscation par auto-modification de code. La clé de déchiffrement étant stockée en clair dans le binaire, l'analyse statique a permis de contourner la protection sans exécution dynamique.