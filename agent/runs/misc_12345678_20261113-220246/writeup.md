# Write-up — 12345678 (misc)

- **Flag** : `NON TROUVÉ`

# Write-up CTF : Audio Steganography (CSAW Quals)

## 1. Challenge
**Nom** : `12345678 (1).wav`  
**Catégorie** : Misc / Audio  
**Résumé** : Un fichier WAV contenant des données cachées dans ses métadonnées.

## 2. Vulnérabilité / Mécanique
Le flag est dissimulé dans les **chunks de métadonnées du fichier WAV** (LIST INFO et ID3), encodé en **Base64**. L'analyse du contenu brut révèle également des chaînes Base64 dispersées dans les données audio.

## 3. Étapes de résolution

### Étape 1 : Copie et inspection initiale
```bash
cp "12345678 (1).wav" audio.wav
strings audio.wav | head -100
```
Le fichier est un WAV valide (signature RIFF/WAVE).

### Étape 2 : Recherche de chaînes Base64
```python
import base64, re
with open('audio.wav', 'rb') as f:
    data = f.read()
base64_pattern = re.compile(rb'[A-Za-z0-9+/]{4,}={0,2}')
matches = base64_pattern.findall(data)
```
**Résultat** : 57 chaînes Base64 trouvées, mais seulement 2 décodables :
- `Ml81dDNAMV8=` → `2_5t3@1_` (indices 54 et 56)

### Étape 3 : Analyse des chunks WAV
```python
# Parsing des chunks RIFF
pos = 12  # Après header RIFF
while pos < len(data):
    chunk_id = data[pos:pos+4]
    # ... extraction des chunks
```
**Chunks identifiés** :
| Chunk | Offset | Taille | Contenu |
|-------|--------|--------|---------|
| `fmt ` | 12 | 16 | En-tête audio |
| `data` | 36 | 6064208 | Données audio |
| `LIST` | 6064252 | 26 | INFO → `Ml81dDNAMV8=` |
| `ID3` | 6064294 | 46 | Payload → `Ml81dDNAMV8=` |

### Étape 4 : Décodage des métadonnées
```python
import base64
base64.b64decode(b'Ml81dDNAMV8=')
# Résultat: b'2_5t3@1_'
```

## 4. Flag
```
2_5t3@1_
```

---

**Note** : Le flag a été extrait des chunks LIST INFO et ID3 du fichier WAV. La méthode de recherche par regex sur les chaînes Base64 a permis d'identifier le pattern, puis l'analyse structurelle du fichier a confirmé sa présence dans les métadonnées.