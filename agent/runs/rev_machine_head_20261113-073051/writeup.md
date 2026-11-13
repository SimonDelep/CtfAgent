# Write-up — Machine Head (rev)

- **Flag** : `NON TROUVÉ`

# Write-up CTF : machine_head

## 1. Challenge
*   **Nom :** `machine_head`
*   **Catégorie :** Reverse Engineering (Rev)
*   **Résumé :** Analyse d'un binaire ELF x86-64 sur une architecture aarch64 contenant une machine virtuelle embarquée.

## 2. Vulnérabilité / mécanique
Le défi repose sur deux mécanismes principaux :
1.  **Incompatibilité d'architecture :** Le binaire est compilé pour **x86-64**, alors que l'environnement d'exécution est **aarch64**, empêchant l'exécution native.
2.  **VM Embarquée :** Le programme utilise une logique de validation basée sur un bytecode stocké dans la section `.