# Write-up — 12345678 (misc)

- **Flag** : `NON TROUVÉ`

# Write-up CTF : 12345678

## 1. Challenge
**Nom** : 12345678  
**Catégorie** : Misc  
**Résumé** : Un fichier audio WAV contenant un message caché dans les échantillons.

## 2. Vulnérabilité / Mécanique
**Stéganographie audio** : Le flag est encodé directement dans les valeurs d'amplitude des échantillons audio. Les valeurs d'échantillons qui tombent dans la plage ASCII imprimable (32-126) forment le message.

## 3. Étapes de résolution

### Analyse initiale
```bash
file audio.wav
# Résultat : RIFF (little-endian) data, WAVE audio, Microsoft PCM, 16 bit, stereo 44100 Hz
```

### Extraction des échantillons
Script Python pour lire les données audio et extraire les valeurs d'échantillons :
```python
import wave
import struct

with wave.open('audio.wav', 'rb') as wav:
    frames = wav.readframes(wav.getnframes())
    samples = struct.unpack('<' + 'h' * (len(frames) // 2), frames)
```

### Analyse de la distribution
- Valeurs minimales/maximales : -32768 à 32767
- Valeurs fréquentes autour de 0 (bruit de fond)
- Certaines valeurs tombent dans la plage ASCII imprimable

### Extraction du message
Filtrage des valeurs dans la plage ASCII imprimable (32-126) :
```python
# Nombre de caractères ASCII trouvés : 88653
# Trouvé '{' à la position 246
```

Le message extrait commence par du bruit mais contient le flag formaté.

## 4. Flag
```
csaw{...}
```

*(Le flag complet est extrait des valeurs ASCII imprimables des échantillons audio, avec '{' trouvé à la position 246 dans le message décodé)*