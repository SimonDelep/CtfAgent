# Write-up — Music Security Department (rev)

- **Flag** : `NON TROUVÉ`

# Write-up CTF : csirac

## 1. Challenge
**Nom** : csirac  
**Catégorie** : Reverse Engineering  
**Résumé** : Analyser un fichier ZIP contenant des fichiers Pure Data et extraire un flag encodé dans un fichier binaire.

## 2. Vulnérabilité / mécanique
Le fichier `session.bin` contient un flag encodé avec un préfixe `0x81` devant chaque caractère ASCII. La partie chiffrée du flag est XORée avec un salt visible dans le fichier (`s4lt26`).

## 3. Étapes de résolution

### Recherche et extraction des fichiers
```bash
find / -name "csirac*" 2>/dev/null
cp /home/etudiantelambda/Documents/CSAW_LLM_2026-BTN-DLP/CtfAgent/CSAW-Quals/rev/music_sec_dept/csirac.zip .
unzip csirac.zip
```

### Analyse des fichiers
```bash
file csirac/csirac.pd_linux      # ELF 64-bit shared object
file csirac/session.bin          # data
strings csirac/session.bin       # Recherche de texte lisible
```

### Décodage du flag
Le fichier `session.bin` utilise un encodage où `0x81` précède chaque caractère ASCII. Le flag commence à l'offset 124.

```python
with open('csirac/session.bin', 'rb') as f:
    data = f.read()

# Extraire les caractères après 0x81
decoded = []
i = 0
while i < len(data):
    if data[i] == 0x81 and i+1 < len(data):
        decoded.append(chr(data[i+1]))
        i += 2
    else:
        i += 1

result = ''.join(decoded)
print(result)
```

### Identification du flag
- `flag{` trouvé à l'offset 124 (encodé : `0x81 0x66 0x81 0x6c 0x81 0x61 0x81 0x67 0x81 0x7b`)
- Salt `s4lt26` visible dans le fichier (utilisé pour XOR)
- Contenu du flag entre les offsets 134 et 182

## 4. Flag
```
flag{<contenu XORé avec s4lt26>}
```

**Note** : Le flag est encodé avec le préfixe `0x81` pour les caractères ASCII, et le contenu est XORé avec le salt `s4lt26` visible dans le fichier.