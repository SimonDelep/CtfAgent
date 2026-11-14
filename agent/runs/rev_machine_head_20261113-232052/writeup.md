# Write-up — Machine Head (rev)

- **Flag** : `NON TROUVÉ`

# Write-up : machine_head

## 1. Challenge
*   **Nom** : `machine_head`
*   **Catégorie** : Reverse Engineering (Rev)
*   **Résumé** : Analyse d'un binaire ELF 64-bit PIE nommé `masterkey` pour retrouver la clé maîtresse (flag).

## 2. Vulnérabilité / mécanique
*   **Analyse binaire** : Le challenge repose sur la compréhension de la logique de vérification d'un exécutable compilé et stripé.
*   **Données cachées** : Le flag (ou la logique de décodage) est stocké dans la section `.rodata` après la chaîne de succès "Correct!".

## 3. Étapes de résolution

1.  **Préparation et identification** :
    *   Copie du fichier `masterkey` dans le répertoire de travail.
    *   Commande `file` et `readelf -h` confirment un **ELF 64-bit LSB PIE** (Position Independent Executable).
    *   L'entrée du programme est située à l'adresse virtuelle `0x1230`.

2.  **Désassemblage** :
    *   Tentative initiale avec `objdump` échouée (problème d'architecture détecté pour un PIE).
    *   Utilisation de **Python avec la librairie `capstone`** pour désassembler manuellement le code à partir de l'offset `0x1230` (correspondant à l'adresse virtuelle car le segment LOAD commence à 0x0).
    *   Analyse du code d'entrée : appel de fonction, vérification de conditions, et branchement vers une routine de vérification.

3.  **Analyse de la section .rodata** :
    *   La section `.rodata` est située à l'adresse virtuelle `0x2000` (offset fichier `0x2000`).
    *   Recherche des chaînes de caractères :
        *   "usage: %s <flag>"
        *   "Wrong."
        *   "Correct! That's the master key."
    *   Observation de données binaires immédiatement après la chaîne "Correct!" (à partir de l'offset `0x2040` dans le fichier, soit `0x2040` dans la section). Ces données (`7a 01 3c 91...`) semblent contenir le flag encodé ou la table de vérification.

4.  **Conclusion** :
    *   Le binaire attend un flag en entrée. La logique de vérification et le message de succès sont identifiés. Le nom du binaire (`masterkey`) et le message de succès indiquent la nature du flag.

## 4. Flag
`CSAW{