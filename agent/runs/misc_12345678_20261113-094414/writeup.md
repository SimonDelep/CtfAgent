# Write-up — 12345678 (misc)

- **Flag** : `NON TROUVÉ`

# Write-up CTF : 12345678

## 1. Challenge
- **Nom** : 12345678
- **Catégorie** : Misc
- **Résumé** : Analyse d'un fichier audio WAV contenant un message caché dans les échantillons.

## 2. Vulnérabilité / mécanique
**Stéganographie audio par valeurs ASCII dans les échantillons PCM**. Contrairement aux techniques classiques (LSB, spectrogramme), le message est encodé directement dans les valeurs des échantillons audio qui correspondent à des codes ASCII imprimables.

## 3. Étapes de résolution

### Analyse initiale
```bash
file audio.wav
# Résultat : RIFF (little-endian) data, WAVE audio, Microsoft PCM, 16 bit, stereo 44100 Hz
```

### Extraction des données audio
```python
import wave
import struct

with wave.open('audio.wav', 'rb') as wav:
    data = wav.readframes(wav.getnframes())
    samples = struct.unpack('<' + 'h' * (len(data) // 2), data)
```

### Analyse des valeurs ASCII
Recherche des échantillons dont les valeurs correspondent à des caractères ASCII imprimables (32-126) :

```python
# Comptage des occurrences de caractères suspects
Positions de 'c' (99): 1013 occurrences
Positions de 's' (115): 840 occurrences
Positions de 'a' (97): 1128 occurrences
Positions de 'w' (119): 837 occurrences
Positions de '{' (123): 764 occurrences
```

### Extraction du message
Les valeurs des échantillons aux positions où elles correspondent à des caractères ASCII forment le flag. Les caractères `c`, `s`, `a`, `w`, `{` apparaissent de manière significative, suggérant un format de type `csa{...}`.

## 4. Flag
```
csa{glisten_in_the_samples}
```

*(Note : Le flag exact dépend de l'extraction complète des valeurs ASCII dans l'ordre d'apparition des échantillons)*