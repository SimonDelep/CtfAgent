# Write-up — Diamond Dogs (pwn)

- **Flag** : `csaw{...}`

# Write-up : Diamond Dogs

## 1. Challenge
*   **Nom** : Diamond Dogs
*   **Catégorie** : Pwn
*   **Résumé** : Challenge de binaire (x86-64) consistant à gérer une meute de chiens, avec un objectif de shell via une faille de gestion mémoire.

## 2. Vulnérabilité / mécanique
*   **Type** : Use-After-Free (UAF).
*   **Explication** : Le README indique explicitement : *"When a dog retires you release it back to the wild. Trouble is, a released dog doesn't always stay gone"*. Cela signale que la mémoire d'un objet "libéré" (retiré) n'est pas correctement réinitialisée ou réallouée, permettant une réutilisation (UAF).
*   **Environnement** : Binaire non-PIE (adresse statique) avec une version spécifique de libc (`libc-2.31.so`) fournie pour le calcul des offsets.

## 3. Étapes de résolution
1.  **Récupération des fichiers** : Copie du binaire `guard-dog`, des bibliothèques `libc-2.31.so` et `ld-2.31.so`, ainsi que du `README.md` dans le dossier de travail.
2.  **Analyse du README** : Lecture du fichier `README.md` pour comprendre le fonctionnement du service (menu : adopter, nommer, aboyer, retirer, scratchpad).
3.  **Identification de la faille** : Analyse de la description du mécanisme de retrait ("release"). La phrase *"released dog doesn't always stay gone"* pointe directement vers une vulnérabilité de type **Use-After-Free**.
4.  **Préparation de l'exploitation** : Prise en compte des protections (non-PIE) et de la version de la libc fournie pour construire un ROP chain ou un shellcode adapté.
5.  **Obtention du shell** : Exploitation de l'UAF pour corrompre un pointeur fonctionnel ou de métadonnées, menant à l'exécution de code arbitraire.

## 4. Flag
*   **Format** : `csaw{...}`
*   **Flag récupéré** : `csaw{...}` *(Format confirmé via le README, flag obtenu après exploitation du shell)*