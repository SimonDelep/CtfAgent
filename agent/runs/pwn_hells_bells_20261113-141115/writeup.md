# Write-up — Hells Bells (pwn)

- **Flag** : `NON TROUVÉ`

# Write-up : Hells Bells

## 1. Challenge
- **Nom** : Hells Bells
- **Catégorie** : Pwn
- **Résumé** : Gestionnaire d'inventaire de charges explosives avec options plant/defuse/rewire/inspect

## 2. Vulnérabilité / mécanique
**Use-After-Free (UAF)** couplé à un **leak libc** et un **overwrite de pointeur**.

Indices du README :
- *"you can't touch a charge once it's defused"* → La charge reste accessible après defuse (UAF)
- *"A defused charge is still sitting right where you left it"* → Mémoire non libérée correctement
- *"One of those leaks where the library lives; the other lets you rewrite a pointer"* → Leak libc + overwrite
- *"There's a hook that runs every time a charge is defused"* → Fonction appelée lors du defuse

## 3. Étapes de résolution

### Analyse initiale
```bash
# Copie des fichiers du challenge
cp README.md thermite-charge libc-2.31.so ld-2.31.so

# Vérification du binaire
file thermite-charge
# → ELF 64-bit LSB pie executable, x86-64, dynamically linked

# Analyse des chaînes
strings thermite-charge | grep -E "(slot|charge|defuse|rewire|inspect|plant|boom|payload)"
```

### Menu identifié
```
1) plant charge
2) defuse charge
3) rewire charge
4) inspect charge
5) leave
```

### Analyse statique
```bash
# Symboles et fonctions
readelf -s thermite-charge | grep -E "(malloc|free)"
# → malloc@@GLIBC_2.2.5, free@@GLIBC_2.2.5

# Tentative de déassemblage
objdump -d thermite-charge 2>/dev/null | head -300
# → Problème d'architecture, nécessite analyse dynamique
```

### Problèmes d'exécution
```bash
# L'interpréteur est ./ld-2.31.so
# Nécessite exécution via le loader fourni
chmod +x ld-2.31.so
./ld-2.31.so --library-path . ./thermite-charge
```

### Script d'interaction (pwntools)
```python
from pwn import *
p = process(['./thermite-charge'], env={'LD_LIBRARY_PATH': '.'})
p.sendlineafter(b'===', b'1')  # plant charge
p.sendlineafter(b'slot', b'0')
p.sendlineafter(b'size', b'10')
```

## 4. Flag
**Statut de la trajectoire** : Analyse en cours, vulnérabilité identifiée (UAF) mais exploitation non finalisée dans la trajectoire fournie.

**Approche recommandée** :
1. Plant une charge dans un slot
2. Defuse la charge (libération partielle)
3. Replant une nouvelle charge dans le même slot (UAF)
4. Utiliser le leak pour obtenir l'adresse libc
5. Overwriter un pointeur via rewire pour obtenir un shell

**Format du flag** : `csaw{...}`