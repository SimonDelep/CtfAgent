# Write-up — Hells Bells (pwn)

- **Flag** : `NON TROUVÉ`

# Write-up : Hells Bells

## 1. Challenge
- **Nom** : Hells Bells
- **Catégorie** : Pwn
- **Résumé** : Gestionnaire d'inventaire de charges thermiques avec options plant/defuse/rewire/inspect.

## 2. Vulnérabilité / mécanique
- **Use-After-Free (UAF)** : La description indique *"you can't touch a charge once it's defused"* — le quartermaster se trompe, une charge défectueuse reste en mémoire.
- **Double fuite** : Une fuite de libc et une réécriture de pointeur sont possibles via les options d'inspection et de reconfiguration.
- **Hook sur defuse** : Un hook s'exécute à chaque détonation, permettant potentiellement de corrompre des pointeurs.

## 3. Étapes de résolution

### Analyse initiale
```bash
# Copie des fichiers du challenge
cp files/thermite-charge .
cp files/libc-2.31.so .
cp files/ld-2.31.so .

# Analyse du binaire
file thermite-charge
# → ELF 64-bit LSB PIE executable, x86-64, dynamically linked
```

### Identification des symboles et fonctions
```bash
nm -D thermite-charge
# Fonctions : main, read_long, read_n, flush
# Variables globales : charges[], sizes[]
```

### Analyse du menu (via strings)
```bash
strings thermite-charge | head -60
# Options : 1) plant charge, 2) defuse charge, 3) rewire charge, 4) inspect charge, 5) leave
```

### Analyse avec GDB
```bash
gdb -q ./thermite-charge -ex "break main" -ex "run" -ex "info functions"
# Adresse main : 0x1318
# Pas de symboles de debug
```

### Tentative d'exécution locale
```bash
chmod +x thermite-charge ld-2.31.so libc-2.31.so
./ld-2.31.so --library-path . ./thermite-charge
# Problème de format d'exécution (architecture incompatible)
```

### Plan d'exploitation (déduit des indices)
1. **Plant** une charge dans un slot
2. **Defuse** la charge (UAF déclenché)
3. **Inspect** pour fuite d'adresse libc
4. **Rewire** pour écraser un pointeur (ex: `free@got`)
5. **Plant** à nouveau pour obtenir un shell

## 4. Flag
```
csaw{...}  # Format attendu (non affiché dans la trajectoire)
```

---

**Note** : La trajectoire montre la phase d'analyse complète (reconnaissance, compréhension du menu, identification de la vulnérabilité UAF), mais s'arrête avant l'exploitation finale. Le binaire nécessite l'interpréteur `ld-2.31.so` fourni pour s'exécuter correctement.