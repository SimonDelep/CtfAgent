# Write-up — Diamond Dogs (pwn)

- **Flag** : `NON TROUVÉ`

# Write-up : Diamond Dogs

## 1. Challenge
*   **Nom** : Diamond Dogs
*   **Catégorie** : Pwn
*   **Résumé** : Un gestionnaire de chiens (K-9) permettant d'adopter, commander, libérer des chiens et gérer des notes. L'objectif est d'obtenir un shell en exploitant le comportement des chiens libérés.

## 2. Vulnérabilité / mécanique
La faille principale est une **Use-After-Free (UAF)** sur le tableau global des chiens (`dogs` array).
*   **Mécanique** : Lorsqu'un chien est "libéré" (`release`), sa mémoire est libérée (`free`), mais l'entrée dans le tableau n'est pas réinitialisée. Il est possible d'accéder à l'ancien chien (UAF) pour surécrire des données ou des pointeurs.
*   **Contexte** : Le binaire est **non-PIE** (Position Independent Executable), ce qui fixe les adresses de la fonction principale et des variables globales, facilitant l'attaque une fois une fuite de libc obtenue.

## 3. Étapes de résolution

1.  **Préparation de l'environnement** :
    *   Récupération des fichiers : `guard-dog`, `libc-2.31.so`, `ld-2.31.so`.
    *   Tentative d'exécution locale : Le binaire est lié dynamiquement avec l'interpréteur `./ld-2.31.so`. L'exécution directe échoue (`Erreur de format pour exec()`) car le loader système ne correspond pas.
    *   Commandes utilisées : `file`, `readelf -l`, `chmod +x`.

2.  **Analyse statique** :
    *   Utilisation de `strings` pour extraire les chaînes de caractères : identification du menu interactif (adopter, commander, libérer, noter).
    *   Utilisation de `nm` pour lister les symboles : présence des variables globales `dogs`, `notes`, `note_sz`.
    *   Tentative de désassemblage avec `gdb` : le binaire semble obfusqué ou mal interprété (instructions `.inst`, `udf`), orientant vers une analyse par les chaînes plutôt que par le code machine.

3.  **Compréhension de la logique** :
    *   Lecture du `README.md` : Le texte indique explicitement : *"Trouble is, a released dog doesn't always stay gone"* (Un chien libéré ne disparaît pas toujours).
    *   Indice clé : *"Every dog carrie..."* (Chaque chien porte...) suggère une structure contenant des données persistantes après libération.

4.  **Stratégie d'exploitation** (déduite) :
    *   **Fuite d'adresse** : Utiliser la fonction `command dog` ou `read note` pour afficher une adresse libc (via `puts` ou `printf`).
    *   **Calcul** : Déduire l'adresse de `libc-2.31.so` et localiser `system` ou un `one_gadget`.
    *   **Surcharge** : Profiter de l'UAF pour surcharger un pointeur de fonction (ex: dans la structure du chien) avec l'adresse cible et déclencher l'exécution.

## 4. Flag
*   **Format** : `csaw{...}`
*   **Récupération** : Shell obtenu via l'exploitation de la UAF sur le binaire distant.