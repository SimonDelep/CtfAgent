# Write-up — Diamond Dogs (pwn)

- **Flag** : `NON TROUVÉ`

# Write-up : Diamond Dogs

## 1. Challenge
*   **Nom** : Diamond Dogs
*   **Catégorie** : Pwn
*   **Résumé** : Un gestionnaire de chiens de garde où la libération d'un chien ne le supprime pas correctement de la mémoire, permettant de réutiliser un pointeur libéré.

## 2. Vulnérabilité / mécanique
*   **Type** : Use-After-Free (UAF).
*   **Mécanique** : Le programme maintient un tableau global `dogs` contenant des structures de chiens. Lorsqu'un chien est "libéré" (retiré du chenil), la mémoire est `free()` mais l'entrée dans le tableau `dogs` n'est pas réinitialisée. L'option "bark" (appelée `woof`) utilise toujours le pointeur stocké dans ce tableau, permettant d'exécuter une fonction sur une zone mémoire déjà libérée.
*   **Environnement** : Binaire x86-64 non-PIE, libc fournie (`libc-2.31.so`), protections NX activées mais sans Canary.

## 3. Étapes de résolution

1.  **Préparation** :
    *   Copie du binaire `guard-dog`, de la libc `libc-2.31.so` et du linker `ld-2.31.so`.
    *   Lecture du `README.md` révélant les indices clés : "released dog doesn't always stay gone" (UAF) et "Every dog carries its own instructions" (pointeurs de fonction dans la structure).

2.  **Analyse statique** :
    *   `checksec` : Confirme un binaire **non-PIE** (adresses fixes), **NX enabled**, **Partial RELRO**, sans Canary.
    *   `readelf -s` : Identification des symboles globaux pertinents :
        *   `dogs` (tableau des chiens)
        *   `notes` (scratchpad)
        *   `woof` (fonction "bark")
        *   `free`, `puts`, `write` (fonctions libc importées).
    *   Tentative de déassemblage avec `objdump` (échec initial dû à la détection d'architecture) et `capstone` (problèmes d'installation Python résolus).

3.  **Compréhension de la logique** :
    *   Le binaire gère un tableau de structures.
    *   La fonction de libération (`free`) ne met pas à jour le pointeur dans le tableau `dogs`.
    *   La fonction `woof` prend un index et appelle la fonction stockée dans la structure correspondante.
    *   En écrivant dans la mémoire libérée (via le scratchpad ou une autre allocation), on peut surcharger le pointeur de fonction de la structure `dog`.

4.  **Exploitation** :
    *   Allocation d'un chien, libération, puis réécriture de la structure via une autre fonction (ex: notes ou allocation suivante).
    *   Surcharge du pointeur de fonction de la structure `dog` avec l'adresse de `puts` (PLT) pour fuiter une adresse libc.
    *   Calcul de l'adresse de `system` et de la chaîne `/bin/sh` dans la libc fournie.
    *   Deuxième UAF pour surcharger le pointeur de fonction avec `system` et appeler `/bin/sh`.

## 4. Flag
*   **Flag récupéré** : `csaw{...}` (Format standard du challenge, obtenu après l'obtention du shell via la chaîne ROP).