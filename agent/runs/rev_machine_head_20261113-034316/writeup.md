# Write-up — Machine Head (rev)

- **Flag** : `NON TROUVÉ`

# Write-up : masterkey

## Challenge
- **Nom** : masterkey
- **Catégorie** : Reverse Engineering
- **Résumé** : Binaire ELF x86-64 exécutant un bytecode personnalisé stocké dans la section .rodata.

## Vulnérabilité / mécanique
Il s'agit d'un **interpréteur de bytecode personnalisé**. Le code x86-64 visible dans le binaire n'est que l'interpréteur ; la logique du programme est encodée en bytecode dans la section `.rodata`, juste après les chaînes de caractères. L'architecture de la machine cible (ARM64) ne correspond pas à celle du binaire (x86-64), forçant une analyse statique.

## Étapes de résolution

1. **Localisation du binaire**
   ```bash
   find / -name "masterkey" 2>/dev/null
   cp /home/etudiantelambda/Documents/CSAW_LLM_2026-BTN-DLP/CtfAgent/CSAW-Quals/rev/machine_head/files/masterkey .
   ```

2. **Analyse initiale**
   ```bash
   file masterkey          # ELF 64-bit LSB pie executable, x86-64
   uname -m                # aarch64 (architecture mismatch)
   ```
   Le binaire est x86-64 mais l'hôte est ARM64. QEMU non disponible → analyse statique.

3. **Extraction des chaînes**
   ```bash
   strings masterkey | head -50
   ```
   Messages clés trouvés :
   - `usage: %s <flag>`
   - `Wrong.`
   - `Correct! That's the master key.`
   - Séquence suspecte : `9*3$"`

4. **Analyse de la structure**
   ```bash
   xxd masterkey | grep -A5 "Correct"
   ```
   Après la chaîne "Correct! That's the master key." (offset `0x2040`), des données binaires commencent :
   ```
   7a 01 3c 91 00 00 7a 00 5a 24 00 11 b2 00 01 7a ...
   ```
   Ces données constituent le bytecode exécuté par l'interpréteur.

5. **Compréhension du mécanisme**
   - Le code x86-64 à l'entrée (`0x1230`) est un interpréteur
   - Le bytecode est stocké en dur dans `.rodata`
   - Le programme compare l'input utilisateur contre une condition définie par le bytecode
   - Pour obtenir le flag, il faut soit :
     - Décompiler le bytecode et comprendre la logique
     - Fournir le bon input qui satisfait la condition du bytecode

## Flag
Le flag n'a pas été extrait dans la trajectoire fournie, mais la séquence `9*3$"` visible dans les strings suggère un format potentiel. La résolution complète nécessiterait de :
1. Décompiler le bytecode à partir de `0x2040`
2. Comprendre les opcodes de l'interpréteur
3. Déduire la condition de validation pour obtenir le flag

**Format probable** : `CSAW{...}` ou similaire, basé sur la séquence `9*3$"` comme indice de structure.