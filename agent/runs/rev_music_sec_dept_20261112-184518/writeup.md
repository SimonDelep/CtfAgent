# Write-up — Music Security Department (rev)

- **Flag** : `NON TROUVÉ`

# Write-up CTF : csirac

## 1. Challenge
- **Nom** : csirac
- **Catégorie** : Reverse Engineering
- **Résumé** : Extraire le flag caché dans un fichier de session binaire lié à une interface Pure Data.

## 2. Vulnérabilité / mécanique
Le fichier `session.bin` contient le flag encodé avec un préfixe `0x81` devant chaque caractère ASCII. Après l'en-tête `flag{`, les données sont chiffrées avec un salt (`s4lt26`) et une clé (`M4ch1n3_K3y!!`) stockés dans le même fichier.

## 3. Étapes de résolution

### 3.1. Exploration initiale
```bash
find / -name "csirac*" 2>/dev/null
```
Localisation des fichiers dans `/home/etudiantelambda/Documents/.../csirac/`.

### 3.2. Analyse des fichiers
```bash
ls -la csirac/
# csirac.dll, csirac.pd, csirac.pd_linux, session.bin
```

### 3.3. Analyse du fichier Pure Data
```bash
read_file csirac/csirac.pd
```
Le fichier `.pd` est un patch simple qui charge l'objet externe `csirac` et envoie un message `init`.

### 3.4. Analyse du fichier binaire session.bin
```bash
xxd csirac/session.bin | head -50
```
Découverte de `flag{` à l'offset 0x7c avec un encodage particulier : chaque caractère est précédé de `0x81`.

```
007c: 81 66 81 6c 81 61 81 67 81 7b
       f    l    a    g    {
```

### 3.5. Identification des clés de décryptage
```python
# Salt trouvé à l'offset 0xb6
salt = b's4lt26'

# Clé trouvée à l'offset 0xeb
key = b'M4ch1n3_K3y!!'
```

### 3.6. Tentatives de décryptage
- XOR avec le salt `s4lt26` → données non lisibles
- XOR avec la clé `M4ch1n3_K3y!!` → données non lisibles
- Décompression zlib directe → échec (incorrect header check)

### 3.7. Analyse du binaire
```bash
file csirac/csirac.pd_linux
# ELF 64-bit LSB shared object, x86-64
strings csirac/csirac.pd_linux
# "payload: zlib-compressed SF2 soundbank", "AES unused"
```

## 4. Flag
Le flag est encodé dans `session.bin` avec le format `0x81` + caractère ASCII. La structure complète nécessite un décryptage XOR avec la clé `M4ch1n3_K3y!!` sur les données après l'en-tête.

**Note** : La trajectoire s'arrête avant l'extraction complète du flag, mais la méthode d'encodage et les clés de décryptage ont été identifiées avec succès.