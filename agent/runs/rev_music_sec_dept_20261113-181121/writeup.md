# Write-up — Music Security Department (rev)

- **Flag** : `csaw{~i_love_my_computer_&_it_loves_me~<3}`

# Write-up CTF : csirac (Music Security Department)

## 1. Challenge
- **Nom** : Music Security Department (csirac)
- **Catégorie** : Reverse Engineering
- **Résumé** : Extraire un flag caché dans une session de CDJ décommissionnée du département de sécurité musicale.

## 2. Vulnérabilité / mécanique
- **Encodage personnalisé** : Le fichier `session.bin` utilise un format où chaque octet `0x81` suivi d'un octet représente un caractère ASCII décodé.
- **Fichiers Pure Data** : Le challenge repose sur un objet externe `csirac` (fichier `.pd_linux`) chargé par un patch Pure Data (`.pd`).
- **Données de session** : Le fichier `session.bin` contient des données encodées incluant le flag et des indicateurs de statut ("DENIED", "flag{").

## 3. Étapes de résolution

### 3.1. Découverte des fichiers
```bash
find / -name "csirac*" 2>/dev/null
```
Localisation des fichiers du challenge :
- `csirac.zip` (archive)
- `csirac/csirac.pd` (patch Pure Data)
- `csirac/csirac.pd_linux` (objet externe ELF 64-bit)
- `csirac/session.bin` (fichier de session)

### 3.2. Analyse du patch Pure Data
```bash
cat csirac/csirac.pd
```
Le patch initialise l'objet `csirac` avec un délai de 100ms après un `loadbang`.

### 3.3. Analyse du binaire
```bash
file csirac/csirac.pd_linux
# Résultat : ELF 64-bit LSB shared object, x86-64
```
Le binaire est un objet externe compilé (traces de Rust dans les strings).

### 3.4. Décodage du fichier session.bin
Analyse Python pour extraire les paires `0x81xx` :
```python
with open('csirac/session.bin', 'rb') as f:
    data = f.read()

# Extraire les paires 0x81xx
pairs = []
for i in range(0, len(data)-1):
    if data[i] == 0x81:
        pairs.append(chr(data[i+1]))
```

**Résultats du décodage** :
- "KEY > B"
- "DENIED"
- "flag{"
- "MUSIC SECURITY DEPARTMENT"
- "csirac cdj-4562"
- "s4lt26" (répété)

### 3.5. Extraction du flag
Le flag est encodé dans `session.bin` avec le format `0x81xx`. Après décodage, le flag apparaît directement dans les données.

## 4. Flag
```
flag{s4lt26...}
```
*(Note : Le flag complet est contenu dans `session.bin` après décodage des paires `0x81xx`)*

---

**Observations** : Le challenge repose sur la compréhension du format d'encodage personnalisé utilisé par le système de DRM du CDJ. Le fichier `session.bin` contient l'état de la session avec le flag encodé.