# Write-up — Saint Vespers and the Copper Choir (pwn)

- **Flag** : `NON TROUVÉ`

# Write-up : Saint Vespers and the Copper Choir

## 1. Challenge
*   **Nom** : Saint Vespers and the Copper Choir
*   **Catégorie** : Pwn
*   **Résumé** : Gestionnaire de choristes avec opérations de recrutement, retraite et restauration, présentant une faille de gestion mémoire.

## 2. Vulnérabilité / mécanique
La faille principale est une **Use-After-Free (UAF)** dans la fonction `op_retire()`.
*   Lors du retrait (`retire`), la structure `chorister` et son `transcript` sont libérés (`free`), mais l'entrée dans le tableau global `choir[idx]` n'est pas mise à `NULL`.
*   La fonction `op_restore()` vérifie si `choir[idx] != NULL` (via `valid_idx`) avant de réactiver un choriste.
*   Comme `choir[idx]` pointe toujours vers la mémoire libérée, un `restore` peut réactiver un pointeur dangling, permettant potentiellement de contrôler la mémoire ou de réallouer un chunk libéré.

## 3. Étapes de résolution
1.  **Récupération des fichiers** : Copie du binaire `vespers`, du code source `vespers.c`, et des bibliothèques dynamiques (`libc.so.6`, `ld-2.35.so`).
2.  **Analyse du code source** : Lecture de `vespers.c` pour comprendre la logique des choristes. Identification de la structure `chorister` et des fonctions `op_retire` / `op_restore`.
3.  **Analyse binaire** : Vérification du type d'exécutable (`ELF 64-bit LSB pie executable`) et de l'interpréteur (`./ld-2.35.so`).
4.  **Tentatives d'exécution locale** :
    *   Lancement direct échoué (`Erreur de format pour exec()`).
    *   Tentative avec `LD_LIBRARY_PATH` et `chmod +x ld-2.35.so`.
    *   Utilisation de `subprocess` en Python pour passer le loader (`ld-2