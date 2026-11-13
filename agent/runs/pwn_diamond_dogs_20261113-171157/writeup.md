# Write-up — Diamond Dogs (pwn)

- **Flag** : `NON TROUVÉ`

# Write-up : Diamond Dogs

## 1. Challenge
- **Nom** : Diamond Dogs
- **Catégorie** : Pwn
- **Résumé** : Un gestionnaire de chiens de garde où l'adoption, le retrait et les notes peuvent mener à une exploitation mémoire.

## 2. Vulnérabilité / mécanique
- **Type** : Use-After-Free (UAF) / Double-Free
- **Logique** : Le programme gère des "chiens" (allocation dynamique) et un "scratchpad" (notes). Lorsqu'un chien est "libéré" (retiré), il n'est pas correctement nettoyé, permettant une réutilisation ou une double libération.
- **Indices** : "When a dog retires you release it back to the wild. Trouble is, a released dog doesn't always stay gone."

## 3. Étapes de résolution

### Analyse initiale
```bash
# Copie des fichiers du challenge
cp files/guard-dog .
cp files/libc-2.31.so .
cp files/ld-2.31.so .

# Vérification du binaire
file guard-dog
# ELF 64-bit LSB executable, x86-64, non-PIE
```

### Problème d'exécution
Le binaire utilise `./ld-2.31.so` comme interpréteur, causant des erreurs d'exécution locale.

```bash
# Correction de l'interpréteur
patchelf --set-interpreter /lib64/ld-linux-x86-64.so.2 guard-dog

# Test d'exécution
./guard-dog
```

### Analyse statique
```bash
# Recherche de chaînes significatives
strings guard-dog | head -100
# Fonctions : malloc, free, read, write, puts, strtol

# Vérification des protections
readelf -S guard-dog | grep -E "\.text|\.data|\.bss"
# .text à 0x401170, non-stripped
```

### Compréhension du mécanisme
D'après le `README.md` :
- Menu interactif : adopter un chien, lui donner un nom, faire aboyer, libérer
- Scratchpad pour les notes
- **Point critique** : Un chien libéré peut rester dans la mémoire

### Hypothèse d'exploitation
1. Adopter un chien → `malloc()`
2. Libérer le chien → `free()` mais pointer non nullifié
3. Réutiliser le même index → UAF
4. Écrire dans le scratchpad pour corrompre les métadonnées
5. Obtenir un shell via `system()` ou `one_gadget` libc

## 4. Flag
```
csaw{...}
```
*(Note : La trajectoire s'arrête à la phase d'analyse. L'exploitation complète nécessite de construire un payload UAF avec les adresses libc fournies.)*

---

**Outils utilisés** : `file`, `readelf`, `strings`, `patchelf`, `gdb`, `pwntools` (disponible)  
**Difficulté** : Medium–Hard  
**Temps estimé** : 1-2h (analyse + exploitation)