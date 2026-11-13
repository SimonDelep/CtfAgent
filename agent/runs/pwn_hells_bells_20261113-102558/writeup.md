# Write-up — Hells Bells (pwn)

- **Flag** : `NON TROUVÉ`

# Write-up CTF : Hells Bells

## 1. Challenge
- **Nom** : Hells Bells
- **Catégorie** : Pwn
- **Résumé** : Gestionnaire d'inventaire de charges thermiques avec opérations plant/defuse/rewire/inspect.

## 2. Vulnérabilité / mécanique
**Use-After-Free (UAF)** : Selon le README, une charge "défusée" reste accessible via les options *rewire* et *inspect* malgré sa suppression logique de l'inventaire. Deux vecteurs d'exploitation sont mentionnés :
1. **Fuite d'adresse** : Révéler l'adresse de la bibliothèque (libc)
2. **Écrasement de pointeur** : Modifier un pointeur que l'allocateur va utiliser

## 3. Étapes de résolution

### 3.1. Récupération des fichiers
```bash
# Copie des fichiers du challenge
thermite-charge, libc-2.31.so, ld-2.31.so, README.md
```

### 3.2. Analyse du README
Le README fournit les indices critiques :
- *"A defused charge is still sitting right where you left it"* → **UAF**
- *"One of those leaks where the library lives"* → **Leak libc**
- *"Rewrite a pointer the allocator is about to trust"* → **Heap manipulation**

### 3.3. Analyse statique du binaire
```bash
file thermite-charge
# ELF 64-bit LSB pie executable, x86-64, dynamically linked

strings thermite-charge | head -100
# Menu : 1) plant charge, 2) defuse charge, 3) rewire charge, 4) inspect charge, 5) leave
```

### 3.4. Problèmes d'exécution locale
Le binaire utilise un interpréteur personnalisé (`ld-2.31.so`) :
```bash
./ld-2.31.so ./thermite-charge
# Erreur : "Erreur de format pour exec()" (ENOEXEC)

patchelf --set-interpreter /lib64/ld-linux-x86-64.so.2 thermite-charge
# Tentative de correction de l'interpréteur
```

### 3.5. Analyse GDB
```bash
gdb -batch -ex "disassemble main" ./thermite-charge
# Instructions illisibles (problème d'architecture ou d'obfuscation)
```

### 3.6. Analyse hexadécimale
```bash
xxd thermite-charge | head -50
# Header ELF valide : 7f 45 4c 46 (ELF64)
```

## 4. Flag
**Statut** : Le flag n'a pas été récupéré dans cette trajectoire (phase d'analyse)

**Flag attendu** : `csaw{...}`

---

## Résumé de l'exploitation (d'après les indices)

| Étape | Action | Objectif |
|-------|--------|----------|
| 1 | Plant une charge | Allouer un chunk |
| 2 | Defuse la charge | Libérer le chunk (mais UAF) |
| 3 | Inspect la charge | Fuite d'adresse (libc) |
| 4 | Rewire la charge | Écraser un pointeur (ex: `__free_hook` ou `tcache`) |
| 5 | Plant une nouvelle charge | Atteindre le pointeur écrasé |
| 6 | Déclencher le hook | Exécuter du code arbitraire → shell |

**Note** : La trajectoire montre une analyse approfondie mais s'arrête avant l'exploitation finale. Le binaire présente des difficultés d'exécution locale (problèmes d'interpréteur/compatibilité libc).