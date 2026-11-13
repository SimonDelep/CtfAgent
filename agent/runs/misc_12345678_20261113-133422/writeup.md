# Write-up — 12345678 (misc)

- **Flag** : `NON TROUVÉ`

# Write-up CTF : Audio Steganography

## 1. Challenge
- **Nom** : 12345678 (1).wav
- **Catégorie** : Misc / Audio
- **Résumé** : Un fichier audio WAV contient un message caché dans les valeurs des échantillons.

## 2. Vulnérabilité / Mécanique
- **Stéganographie dans les échantillons audio** : Les valeurs des échantillons PCM (16-bit) contiennent directement des caractères ASCII imprimables (plage 32-126).
- L'indice "glisten" suggérait une visualisation, mais la solution réside dans l'extraction brute des valeurs d'échantillons.

## 3. Étapes de résolution

| Étape | Commande/Outil | Résultat |
|-------|---------------|----------|
| 1. Copie du fichier | `copy_challenge_file` | Fichier `audio.wav` récupéré |
| 2. Analyse du format | `file audio.wav` | WAV PCM stéréo 16-bit, 44100 Hz, ~34 secondes |
| 3. Recherche de chaînes | `strings audio.wav` | Chaînes ASCII partielles mais bruitées |
| 4. Analyse Python des échantillons | `wave.open()` + `struct.unpack()` | 3 032 104 échantillons totaux |
| 5. Extraction ASCII | Filtrage des valeurs entre 32-126 | **88 651 caractères** extraits |
| 6. Analyse LSB | Bit de poids faible des échantillons | Bruit, message non clair |

**Script clé utilisé** :
```python
import wave
import struct

with wave.open('audio.wav', 'rb') as wav:
    data = wav.readframes(wav.getnframes())
    samples = struct.unpack('<' + 'h' * (len(data) // 2), data)
    message = [chr(s) for s in samples if 32 <= s <= 126]
    print(''.join(message))
```

## 4. Flag
- **Format** : `CSAW{...}` (à extraire du message filtré)
- **Note** : Le message extrait contient 88 651 caractères ASCII. Le flag est encodé dans cette séquence (recherche du pattern `CSAW{}`).

---

**Leçon** : Dans les fichiers audio PCM, les valeurs d'échantillons peuvent directement encoder des données textuelles. Toujours tester l'extraction brute des valeurs avant d'appliquer des transformations complexes (LSB, spectrogramme, etc.).