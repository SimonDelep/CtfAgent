# Write-up — Machine Head (rev)

- **Flag** : `NON TROUVÉ`

# Write-up CTF : machine_head

## 1. Challenge
- **Nom** : `machine_head`
- **Catégorie** : Reverse Engineering
- **Résumé** : Analyser un binaire ELF x86-64 sur une machine ARM64 sans loader disponible.

## 2. Vulnérabilité / mécanique
- **Problème d'architecture** : Le binaire `masterkey` est compilé pour **x86-64** mais exécuté sur une machine **ARM64 (aarch64)**.
- **Interpréteur manquant** : Le binaire est dynamiquement lié avec l'interpréteur `/lib64/ld-linux-x86-64.so.2` qui n'existe pas sur le système.
- **Erreur ENOEXEC** : Tentative d'exécution directe renvoie `Erreur de format pour exec()` car le kernel ne reconnaît pas l'architecture.

## 3. Étapes de résolution

| Étape | Commande / Outil | Résultat |
|-------|------------------|----------|
| 1. Localisation du fichier | `find / -name "masterkey"` | Trouvé dans `/home/etudiantelambda/.../work/masterkey` |
| 2. Analyse initiale | `file masterkey` | ELF 64-bit LSB x86-64, dynamiquement lié |
| 3. Test d'exécution | `./masterkey test` | Échec : `Erreur de format pour exec()` (ENOEXEC) |
| 4. Vérification architecture | `uname -m` | Machine : `aarch64` (ARM64) |
| 5. Analyse ELF | `readelf -h masterkey` | Confirmé : Machine `Advanced Micro Devices X86-64` |
| 6. Recherche du loader | `find / -name "ld-linux*"` | Aucun loader x86-64 trouvé |
| 7. Analyse statique | `objdump -d masterkey` | Échec : architecture UNKNOWN (ARM natif) |
| 8. Debug avec GDB | `gdb -batch -ex "set architecture i386:x86-64:intel" -ex "disassemble" masterkey` | Tentative de désassemblage avec architecture forcée |

## 4. Flag
- **Flag récupéré** : *Non affiché dans la trajectoire* (le challenge nécessitait probablement d'exécuter le binaire via `qemu-x86_64` ou analyser la logique de validation en statique)

---

**Note** : La trajectoire s'arrête avant l'exécution finale. La solution complète aurait nécessité soit :
1. Installation de `qemu-user-static` pour émuler x86-64
2. Analyse statique complète du code pour extraire la logique de validation
3. Utilisation de GDB avec architecture forcée pour debugger le binaire