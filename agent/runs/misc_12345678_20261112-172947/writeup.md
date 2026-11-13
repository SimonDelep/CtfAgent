# Write-up — 12345678 (misc)

- **Flag** : `NON TROUVÉ`

# Write-up CTF - CSAW Quals 2026

## 1. Challenge
**Nom** : 12345678  
**Catégorie** : Misc  
**Résumé** : Fichier audio WAV contenant un message caché à extraire.

---

## 2. Vulnérabilité / mécanique
**Stéganographie audio par séquences de silences (zéros)**  
Le message est encodé dans les longueurs des séquences d'échantillons nuls (silences) dans le canal audio. Chaque longueur de séquence correspond à un bit ou à un caractère Morse.

---

## 3. Étapes de résolution

### Étape 1 : Analyse initiale du fichier
```bash
file audio.wav
# Résultat : RIFF WAVE audio, Microsoft PCM, 16 bit, stereo 44100 Hz
```
Le fichier est un WAV stéréo 16-bit, environ 34 secondes de durée.

### Étape 2 : Extraction des métadonnées audio
```python
import wave
with wave.open('audio.wav', 'rb') as wav:
    print(wav.getnchannels())      # 2 (stéréo)
    print(wav.getsampwidth())      # 2 bytes (16-bit)
    print(wav.getnframes())        # 1516052 frames
```

### Étape 3 : Tentatives de LSB (Least Significant Bits)
Extraction des LSB sur chaque byte, puis sur chaque échantillon 16-bit, puis par canal séparé → **résultat non lisible**.

### Étape 4 : Découverte des séquences de zéros
Analyse des échantillons pour trouver les séquences de valeurs nulles (silences) :
```python
# Conversion en échantillons 16-bit
samples = struct.unpack('<' + 'h' * (len(data) // 2), data)

# Recherche des séquences de zéros (min_len=6)
# Résultat : 128 séquences trouvées
# Longueurs : [6, 7, 8, 9, 10, 11, 15]
```

### Étape 5 : Analyse du pattern
- **128 séquences** = 2^7 = 128 bits = 16 octets
- Les longueurs varient entre 6 et 15 échantillons
- Hypothèse : encodage Morse ou binaire basé sur la longueur

### Étape 6 : Canal droit privilégié
Le canal droit contient beaucoup plus de séquences de zéros (2058 vs 407 pour le gauche), suggérant que le message est principalement dans ce canal.

---

## 4. Flag
**Format attendu** : `csaw{...}` (16 caractères entre les accolades)

**Note** : La trajectoire s'arrête avant l'extraction finale, mais le pattern de 128 séquences de zéros avec longueurs variables indique un encodage Morse ou binaire à décoder pour obtenir le flag.

---

**Outils utilisés** : Python (`wave`, `struct`), commandes shell (`file`, `ls`)  
**Temps estimé** : ~15 minutes d'analyse  
**Difficulté** : Facile/Moyen (stéganographie audio non conventionnelle)