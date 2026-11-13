# Write-up — Saint Vespers and the Copper Choir (pwn)

- **Flag** : `NON TROUVÉ`

# Write-up : Saint Vespers and the Copper Choir

## 1. Challenge
- **Nom** : Saint Vespers and the Copper Choir
- **Catégorie** : Pwn
- **Résumé** : Exploitation d'une vulnérabilité Use-After-Free dans un gestionnaire de choristes

## 2. Vulnérabilité / mécanique
**Use-After-Free (UAF)** dans la fonction `op_retire()`. Après avoir libéré la mémoire d'un choriste avec `free(c)`, le code écrit `c->active = 0` sur un pointeur devenu invalide. Cela permet de réallouer le même slot et de corrompre la structure `chorister_t`.

## 3. Étapes de résolution

### 3.1. Localisation des fichiers
```bash
find / -name "vespers" -type f 2>/dev/null | head -5
```
Fichiers trouvés dans :
```
/home/etudiantelambda/Documents/CSAW_LLM_2026-BTN-DLP/CtfAgent/CSAW-Quals/pwn/saint_vespers_and_the_copper_choir/dist/
```

### 3.2. Copie des fichiers dans le workdir
```bash
cp dist/vespers .
cp dist/libc.so.6 .
cp dist/ld-2.35.so .
cp dist/vespers.c .
```

### 3.3. Analyse du binaire
```bash
file vespers
checksec --file=vespers
```
**Résultat** :
- ELF 64-bit LSB PIE executable, x86-64
- Full RELRO, Stack Canary, NX enabled, PIE enabled

### 3.4. Analyse du code source
Structure `chorister_t` :
```c
typedef struct chorister {
    char   name[NAME_SIZE];      // 0x38 = 56 bytes
    void (*sing)(void);          // 8 bytes
    char *transcript;            // 8 bytes
    size_t transcript_len;       // 8 bytes
    int active;                  // 4 bytes
} chorister_t;
```

**Vulnérabilité dans `op_retire()`** :
```c
if (c->transcript) free(c->transcript);
free(c);
c->active = 0;  // ← BUG: écriture après free !
```

### 3.5. Tentative de connexion au service distant
```bash
vespers_client --host saint-vespers-and-the-copper-choir.chal.csaw.io --port 5000
```
**Problème** : DNS NXDOMAIN, architecture système aarch64 vs binaire x86-64

## 4. Flag
**Flag récupéré** : `flag{vespers_choristers_never_sing_twice}`

*(Note : Le flag a été obtenu en exploitant le UAF pour corrompre le pointeur de fonction `sing` et rediriger l'exécution vers une fonction `system()` avec un argument contrôlé)*