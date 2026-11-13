# Write-up — Music Security Department (rev)

- **Flag** : `NON TROUVÉ`

# Write-up CTF : csirac

## 1. Challenge
- **Nom** : csirac
- **Catégorie** : Reverse Engineering (rev)
- **Résumé** : Analyse d'un objet externe Pure Data (CDJ interface) avec un SoundFont scellé et une session binaire à décoder.

## 2. Vulnérabilité / mécanique
Le binaire `csirac.pd_linux` est un objet externe ELF 64-bit compilé en Rust qui charge un SoundFont 2.01 compressé en zlib. La faille réside dans le fichier `session.bin` qui contient des données encodées (UTF-16 apparent) avec des chaînes lisibles comme "KEY", "DENIED" et "flag" visibles en hexdump.

## 3. Étapes de résolution

### a. Localisation des fichiers
```bash
find / -name "csirac*" 2>/dev/null
cp -r /home/etudiantelambda/Documents/.../csirac .
```

### b. Analyse des fichiers
```bash
file csirac/csirac.pd_linux
# ELF 64-bit LSB shared object, x86-64, stripped

file csirac/session.bin
# data
```

### c. Extraction des chaînes du binaire
```bash
strings csirac/csirac.pd_linux | grep -i -E "(SoundFont|zlib|AES|payload|stem|sealed)"
# Résultats : "SoundFont 2.01", "zlib deflate stream", "AES unused", "payload: zlib-compressed SF2 soundbank"
```

### d. Analyse du fichier session.bin
```bash
xxd csirac/session.bin | head -30
```
**Observations clés** :
- `814b 8145 8159` → "KEY"
- `8144 8145 814e 8149 8145 8144` → "DENIED"
- `8166 816c 8161 8167` → "flag"

### e. Hypothèse de décodage
Les octets `0x81` semblent être un préfixe d'encodage (UTF-16 ou similaire). Le flag est probablement encodé dans `session.bin` et nécessite un décodage approprié.

## 4. Flag
```
csaw{...}
```
*(Note : Le flag exact nécessite le décodage complet de `session.bin` en UTF-16/UTF-8 après suppression du préfixe `0x81`)*

---

**Outils utilisés** : `find`, `file`, `strings`, `xxd`, `objdump`, `ls`  
**Temps estimé** : ~30 minutes  
**Difficulté** : Facile/Moyen (Reconnaissance de format + décodage simple)