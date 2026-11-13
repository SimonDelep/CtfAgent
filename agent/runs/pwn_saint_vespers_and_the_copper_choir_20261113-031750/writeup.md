# Write-up — Saint Vespers and the Copper Choir (pwn)

- **Flag** : `NON TROUVÉ`

# Write-up : Saint Vespers and the Copper Choir

## 1. Challenge
- **Nom** : Saint Vespers and the Copper Choir
- **Catégorie** : PWN
- **Résumé** : Exploitation d'une faille use-after-free dans un gestionnaire de choristes

## 2. Vulnérabilité / mécanique
**Use-After-Free (UAF)** dans le mécanisme `retire()` / `restore()` :
- `op_retire()` libère la structure `chorister` et son `transcript`, mais **ne met pas à NULL** `choir[idx]`
- `op_restore()` vérifie `choir[idx] != NULL` puis réactive le même pointeur déjà libéré
- Taille de la structure : ~96 bytes (`0x60`)

## 3. Étapes de résolution

| Étape | Action | Commande/Outil |
|-------|--------|----------------|
| 1 | Récupération des fichiers | `copy_challenge_file` (vespers, vespers.c, libc.so.6, ld-2.35.so) |
| 2 | Analyse du code source | `read_file` vespers.c |
| 3 | Analyse du binaire | `checksec --file=vespers` |
| 4 | Identification UAF | Analyse manuelle de `op_retire()` et `op_restore()` |
| 5 | Vérification protections | PIE, Full RELRO, NX, Canary, FORTIFY, SHSTK, IBT |
| 6 | Test local | `process('./vespers', env={'LD_LIBRARY_PATH': '.'})` |

**Protections détectées** :
```
RELRO:      Full RELRO
Stack:      Canary found
NX:         NX enabled
PIE:        PIE enabled
FORTIFY:    Enabled
SHSTK:      Enabled
IBT:        Enabled
```

## 4. Flag
- **Statut** : En cours d'exploitation au moment de la trajectoire
- **Format attendu** : `csaw{...}`

---

**Note** : La trajectoire s'est arrêtée à la phase d'analyse de la vulnérabilité. L'exploitation complète nécessiterait :
1. Allouer un nouveau chorister pour surécrire la structure libérée
2. Fuite d'adresse libc via `sing` callback
3. ROP pour contourner les protections (PIE + Canary)