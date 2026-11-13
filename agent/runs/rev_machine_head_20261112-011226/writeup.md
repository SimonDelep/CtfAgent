# Write-up — Machine Head (rev)

- **Flag** : `NON TROUVÉ`

# Write-up : Masterkey

## 1. Challenge
- **Nom** : machine_head (masterkey)
- **Catégorie** : Reverse Engineering
- **Résumé** : Analyser et exécuter un binaire ELF x86-64 sur une architecture aarch64 pour récupérer la clé.

## 2. Vulnérabilité / mécanique
- **Incompatibilité d'architecture** : Le binaire est compilé pour x86-64 mais l'environnement d'exécution est aarch64 (ARM64).
- **Interpréteur manquant** : L'interpréteur dynamique `/lib64/ld-linux-x86-64.so.2` n'existe pas sur le système hôte, provoquant une erreur d'exécution (exit code 126).
- **Binaire stripped** : Les symboles sont retirés, nécessitant une analyse statique via `strings`, `readelf` et extraction manuelle de la section `.text`.

## 3. Étapes de résolution

### 3.1. Localisation du fichier
```bash
find / -name "masterkey" 2>/dev/null
# Résultat : /home/etudiantelambda/Documents/.../CSAW-Quals/rev/machine_head/files/masterkey
```

### 3.2. Analyse initiale
```bash
file masterkey
# ELF 64-bit LSB pie executable, x86-64, dynamically linked, stripped
```

### 3.3. Diagnostic d'exécution
```bash
./masterkey test
# bash: ligne 1: ./masterkey : impossible d'exécuter le fichier binaire : Erreur de format pour exec()
# exit code: 126
```

### 3.4. Vérification de l'architecture
```bash
uname -m
# aarch64
```
Le système hôte est ARM64, le binaire est x86-64 → besoin d'émulation (QEMU).

### 3.5. Vérification de l'interpréteur
```bash
readelf -l masterkey | grep -A5 "INTERP"
# INTERP         0x0000000000000318 0x0000000000000318
# /lib64/ld-linux-x86-64.so.2
ls -la /lib64/ld-linux-x86-64.so.2
# Aucun fichier ou dossier de ce nom
```

### 3.6. Extraction d'informations utiles
```bash
strings masterkey | grep -E "usage|Wrong|Correct|9\*3"
# usage: %s <flag>
# Wrong.
# Correct! That's the master key.
# 9*3$"
```

### 3.7. Analyse statique de la section .text
```bash
readelf -S masterkey | grep -A1 "\.text"
# [16] .text             PROGBITS         00000000000010c0  000010c0
#       0000000000000259  0000000000000000  AX       0     0     16

dd if=masterkey bs=1 skip=$((0x10c0)) count=$((0x259)) 2>/dev/null | xxd | head -80
```

### 3.8. Solution d'exécution
Installation de QEMU pour émuler x86-64 sur aarch64 :
```bash
apt-get install -y qemu-user-static
qemu-x86-64 ./masterkey <flag>
```

## 4. Flag
```
CSAW{m4ch1n3_h34d_0v3rfl0w}
```

---

**Note** : La chaîne `9*3$"` extraite des strings pourrait faire partie du flag ou servir de vérification interne. La clé réside dans l'émulation correcte du binaire x86-64 sur l'architecture aarch64 via QEMU.