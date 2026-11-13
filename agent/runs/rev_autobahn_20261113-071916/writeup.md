# Write-up — Autobahn (rev)

- **Flag** : `NON TROUVÉ`

# Write-up : Nitro

## 1. Challenge
- **Nom** : Nitro
- **Catégorie** : Reverse Engineering (rev)
- **Résumé** : Binaire ELF x86-64 avec une section de code chiffrée à décrypter pour obtenir le flag.

## 2. Vulnérabilité / mécanique
- **Self-Modifying Code (SMC)** : Le binaire contient une section `enccode` chiffrée qui doit être déchiffrée à l'exécution par le code d'entrée.
- **Magic Numbers** : Présence de motifs `baad f00d`, `c0de`, `1337` dans la section chiffrée, suggérant un algorithme de chiffrement simple.
- **Problème d'exécution** : Le binaire renvoie `ENOEXEC` (Erreur de format pour exec()) au lancement direct, probablement dû à des alignements ou flags de segment inhabituels.

## 3. Étapes de résolution

### Analyse initiale
```bash
cp /home/etudiantelambda/Documents/CSAW_LLM_2026-BTN-DLP/CtfAgent/CSAW-Quals/rev/autobahn/files/nitro .
file nitro
# ELF 64-bit LSB executable, x86-64, dynamically linked, not stripped
```

### Recherche de chaînes
```bash
strings nitro | head -50
# "NITRO ENGAGED: %s"
# "usage: %s <password>"
# "Access denied. The engine stays cold."
# "enc_flag"
```

### Analyse des sections
```bash
readelf -S nitro | grep -A1 enccode
# [16] enccode PROGBITS 000000000040130d 0000130d
# Taille: 0x15e (350 octets), Flags: AX (allocatable, executable)
```

### Examen du code chiffré
```bash
xxd -s 0x130d -l 0x15e nitro
# Motifs observés: baad f00d, baad f0ca, c0de, 1337
```

### Tentatives d'exécution
```bash
./nitro test
# Exit code: 126 (ENOEXEC - Erreur de format pour exec())
strace -e trace=execve ./nitro test
# execve("./nitro", ...) = -1 ENOEXEC
```

### Analyse du point d'entrée
```bash
xxd -s 0x10f0 -l 200 nitro
# Code valide x86-64: endbr64, xor ebp, ebp, etc.
```

### Problèmes rencontrés
- `objdump -d` échoue avec "UNKNOWN architecture"
- GDB timeout lors du débogage
- Le binaire semble avoir besoin d'un environnement d'exécution spécifique

## 4. Flag
- **Statut** : Non récupéré dans la trajectoire
- **Indice** : Le flag est probablement stocké dans la variable `enc_flag` et doit être déchiffré après exécution réussie du code dans la section `enccode`.

## Conclusion
Le challenge repose sur l'analyse d'un binaire avec code auto-déchiffrant. La section `enccode` contient le code principal chiffré, qui doit être déchiffré dynamiquement par le code d'entrée. Le flag serait affiché après un mot de passe correct. La difficulté principale réside dans le contournement du problème d'exécution (`ENOEXEC`) et la compréhension du mécanisme de déchiffrement.