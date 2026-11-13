# Write-up — Machine Head (rev)

- **Flag** : `NON TROUVÉ`

# Write-up CTF : Machine Head

## 1. Challenge
**Nom** : `masterkey`  
**Catégorie** : Reverse Engineering  
**Résumé** : Binaire ELF x86-64 exécutant une VM personnalisée sur une architecture ARM64.

## 2. Vulnérabilité / Mécanique
- **Incompatibilité d'architecture** : Le binaire est compilé en **x86-64** mais exécuté sur une machine **aarch64** (ARM64).
- **VM personnalisée** : Le code x86-64 interprète des **bytecodes** stockés dans la section `.rodata` du binaire.
- **Analyse statique nécessaire** : QEMU n'étant pas installé, l'exécution dynamique est difficile, forçant une analyse statique.

## 3. Étapes de résolution

### Recherche du binaire
```bash
find / -name "masterkey" 2>/dev/null
```
Le fichier se trouve dans un chemin profond, copié localement avec `copy_challenge_file`.

### Identification de l'architecture
```bash
file masterkey
# ELF 64-bit LSB pie executable, x86-64
uname -m
# aarch64
```
**Problème** : Architecture hôte (aarch64) ≠ architecture cible (x86-64).

### Tentative d'exécution
```bash
./masterkey test
# Erreur de format pour exec()
qemu-x86_64 ./masterkey test
# Commande introuvable (QEMU non installé)
```

### Analyse statique
```bash
strings masterkey
# "usage: %s <flag>", "Wrong.", "Correct! That's the master key."
readelf -S masterkey
# Section .rodata à 0x2000, taille 0x7ba octets
```

### Extraction du bytecode
```bash
dd if=masterkey bs=1 skip=$((0x2000)) count=$((0x7ba)) 2>/dev/null | xxd
```
Après les chaînes de caractères (à partir de `0x2040`), des données structurées apparaissent :
- `7a 01`, `7a 00`, `b2 00`, `a7 00`, `6d 01` → opcodes
- `3c 91 00 00`, `5a 24 00 11` → opérandes

### Conclusion de l'analyse
Le binaire implémente une **VM personnalisée** qui :
1. Lit le flag en argument
2. Exécute un bytecode stocké dans `.rodata`
3. Compare le résultat avec une valeur attendue
4. Affiche "Correct!" ou "Wrong."

## 4. Flag
Le flag n'est pas explicitement affiché dans la trajectoire, mais le format attendu est :
```
CSAW{...}
```
*(Le flag exact nécessiterait la reconstruction de la VM ou l'installation de QEMU pour exécution dynamique)*

---

**Outils utilisés** : `file`, `find`, `strings`, `readelf`, `xxd`, `dd`, `objdump`  
**Difficulté** : Moyen (analyse de VM + cross-architecture)  
**Temps estimé** : 30-45 minutes