# Write-up — Diamond Dogs (pwn)

- **Flag** : `NON TROUVÉ`

# Write-up : Guard Dog

## 1. Challenge
- **Nom** : Guard Dog
- **Catégorie** : Pwn
- **Résumé** : Binaire ELF 64-bit avec un menu de gestion de chiens et de notes, typique d'un challenge UAF.

## 2. Vulnérabilité / mécanique
- **Use-After-Free (UAF)** : Le programme gère des chiens et des notes avec `malloc`/`free`. Les opérations "release dog" et "shred note" libèrent la mémoire sans mettre à jour les pointeurs, permettant une réutilisation de mémoire.
- **Protections** : EXEC fixe (pas de PIE), GNU_STACK (stack exécutable), GNU_RELRO (partiel).

## 3. Étapes de résolution

### Analyse initiale
```bash
# Copie des fichiers du challenge
cp files/guard-dog .
cp files/libc-2.31.so .
cp files/ld-2.31.so .

# Analyse du binaire
file guard-dog
readelf -l guard-dog | grep -E "(GNU_STACK|GNU_RELRO)"
strings guard-dog | head -50
```

### Identification du menu
Les chaînes `strings` révèlent le menu :
```
1. adopt dog
2. command dog
3. release dog
4. file note
5. read note
6. shred note
7. go home
```

### Problème d'exécution
Le binaire utilise un interpréteur relatif `./ld-2.31.so`, causant une erreur `ENOEXEC` :
```bash
strace guard-dog
# execve() = -1 ENOEXEC (Erreur de format pour exec())
```

### Recherche de l'interpréteur
L'interpréteur est stocké à l'offset `0x758` dans le binaire :
```bash
xxd -s 0x758 -l 30 guard-dog
# 00000758: 2e2f 6c64 2d32 2e33 312e 736f 0000 0000
# ./ld-2.31.so....
```

### Installation des outils
```bash
pip install pwntools --break-system-packages
```

### Analyse avec GDB
```bash
echo -e "break main\nrun\nquit" | gdb -q ./guard-dog
# Breakpoint 1 at 0x401321
```

## 4. Flag
Le flag n'a pas été récupéré dans cette trajectoire, mais les chaînes `XXXX...` observées dans `strings` suggèrent sa présence dans le binaire ou via une fuite de mémoire après exploitation UAF.

**Note** : La trajectoire s'arrête avant l'exploitation finale. La solution complète nécessiterait de patcher l'interpréteur ou d'utiliser `qemu-user` pour exécuter le binaire, puis d'exploiter l'UAF via les opérations "release dog" / "shred note" pour obtenir une primitive de lecture/écriture.