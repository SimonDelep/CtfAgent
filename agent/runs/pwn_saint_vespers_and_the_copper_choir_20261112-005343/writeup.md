# Write-up — Saint Vespers and the Copper Choir (pwn)

- **Flag** : `NON TROUVÉ`

# Write-up : Saint Vespers and the Copper Choir

## 1. Challenge
- **Nom** : Saint Vespers and the Copper Choir
- **Catégorie** : PWN
- **Résumé** : Exploitation d'une Use-After-Free dans un gestionnaire de choristes.

## 2. Vulnérabilité / mécanique
**Use-After-Free (UAF)** dans la fonction `op_retire()`.

Après avoir libéré la mémoire d'un choriste avec `free(c)`, le code écrit `c->active = 0` sur une mémoire déjà libérée :

```c
if (c->transcript) free(c->transcript);
free(c);
c->active = 0;  // BUG: c est déjà free'd !
```

Le pointeur `choir[idx]` reste valide (dangling pointer), permettant de réallouer la même adresse et de corrompre les champs de la structure.

## 3. Étapes de résolution

| Étape | Action | Détail |
|-------|--------|--------|
| 1 | Récupération des fichiers | Copie du binaire `vespers`, source `vespers.c`, `libc.so.6` et `ld-2.35.so` |
| 2 | Analyse du code source | Lecture de `vespers.c` pour comprendre la structure `chorister_t` |
| 3 | Analyse de la structure | `chorister_t` contient : `name[0x38]`, `sing` (pointeur fonction), `transcript`, `transcript_len`, `active` (total ~84-96 bytes) |
| 4 | Identification du bug | Dans `op_retire()`, `free(c)` est suivi de `c->active = 0` sur mémoire libérée |
| 5 | Plan d'exploitation | 1. Recruter choriste (slot 0) → 2. Retirer (free) → 3. Recruter nouveau choriste (réutilise la même adresse) → 4. Le nouveau aura `active=0` corrompu → 5. Manipuler `transcript` ou `sing` pour RCE |
| 6 | Test de connexion | Tentative de connexion au service distant (DNS non résolu dans l'environnement) |

## 4. Flag
- **Flag** : Non récupéré dans cette trajectoire (service distant inaccessible via DNS)

---

**Note** : L'exploitation complète nécessiterait de contourner le problème DNS, puis d'utiliser l'UAF pour corrompre le pointeur de fonction `sing` ou le pointeur `transcript` afin d'obtenir un contrôle de flux et exécuter du code arbitraire.