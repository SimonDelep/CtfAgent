# Write-up — Autobahn (rev)

- **Flag** : `NON TROUVÉ`

# Write-up CTF : nitro

## 1. Challenge
*   **Nom** : `nitro`
*   **Catégorie** : Reverse Engineering (Rev)
*   **Résumé** : Analyse d'un binaire ELF x86-64 contenant une section de code chiffrée, exécuté sur une machine hôte ARM64.

## 2. Vulnérabilité / mécanique
La protection repose sur deux mécanismes :
1.  **Incompatibilité d'architecture** : Le binaire est compilé pour **x86-64**, tandis que l'environnement d'exécution est **aarch64** (ARM64), bloquant l'exécution native.
2.  **Code auto-modifiant (SMC) / Chiffrement** : Une section personnalisée nommée `enccode` (flags `AX` : Allocatable + Executable) contient le code principal chiffré. Ce code doit être déchiffré dynamiquement par le code de la section `.text` avant exécution.

## 3. Étapes de résolution

1.  **Identification du fichier** :
    *   Copie du fichier `nitro` dans le dossier de travail.
    *   Commande `file` : Confirme un exécutable ELF 64-bit x86-64, non stripé.
    *   Commande `strings` : Révèle des chaînes de caractères indicatives (`usage: %s <password>`, `NITRO ENGAGED: %s`, `enc_flag`, `smc_key.0`, `enccode`).

2.  **Diagnostic d'exécution** :
    *   Tentative d'exécution directe (`./nitro`) : Échec avec "Erreur de format pour exec()".
    *   Commande `uname -m` : Confirme que l'hôte est `aarch64`.
    *   Tentative d'installation de `qemu-user-static` pour émuler x86-64 : Bloquée par des problèmes de permissions (`apt-get` lock).

3.  **Analyse statique approfondie** :
    *   Commande `readelf -S` : Identification des sections.
    *   Découverte de la section `enccode` :
        *   Offset : `0x