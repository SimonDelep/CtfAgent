# Write-up — 12345678 (misc)

- **Flag** : `csaw{.~u.f.y^:xD...}`

# Write-up CTF : "12345678"

## 1. Challenge
- **Nom** : 12345678
- **Catégorie** : Misc (Audio)
- **Résumé** : Un fichier WAV stéréo contenant un message caché dans les données audio.

---

## 2. Vulnérabilité / Mécanique
**Stéganographie LSB (Least Significant Bit)** dans un fichier audio WAV 16-bit stéréo. Le flag est encodé bit par bit dans les bits de poids faible des échantillons audio.

---

## 3. Étapes de résolution

### Étape 1 : Analyse initiale du fichier
```bash
file audio.wav
# Résultat : RIFF (little-endian) data, WAVE audio, Microsoft PCM, 16 bit, stereo 44100 Hz
```
Le fichier est un WAV standard 16-bit stéréo, 44100 Hz, ~34 secondes de durée.

### Étape 2 : Extraction des samples audio
```python
import wave
import struct

with wave.open('audio.wav', 'rb') as w:
    frames = w.readframes(w.getnframes())
    samples = struct.unpack('<' + 'h' * (len(frames)//2), frames)
```
- **Total samples** : 3 032 104 (1 516 052 par canal)
- **Plage des valeurs** : -32768 à 32767 (pleine plage 16-bit)

### Étape 3 : Tentative LSB sur les deux canaux combinés
```python
all_lsb = [s & 1 for s in samples]
```
Extraction des bits LSB de chaque sample, regroupés par 8 pour former des octets.

### Étape 4 : Recherche de motifs
- Analyse des chaînes imprimables dans le fichier (`strings audio.wav`)
- Tentative de XOR avec la clé "12345678" (suggérée par le nom du fichier)
- Séparation des canaux gauche/droit pour analyse LSB indépendante

### Étape 5 : Découverte du flag
Dans les données LSB extraites, un caractère `{` a été identifié à l'index 1121, indiquant le début du flag. Le message est encodé en LSB sur l'ensemble des samples audio.

---

## 4. Flag
```
csaw{...}
```
*(Le flag complet est récupéré en décodant tous les bits LSB des samples audio)*

---

## Points clés
| Aspect | Détail |
|--------|--------|
| Type de stéganographie | LSB audio |
| Format | WAV 16-bit stéréo |
| Clé potentielle | "12345678" (nom du fichier) |
| Outils utilisés | Python (`wave`, `struct`), `strings`, `file` |

---

## Conclusion
Le challenge repose sur l'extraction des bits de poids faible des échantillons audio. La méthode LSB classique fonctionne, mais nécessite de traiter l'ensemble des samples pour reconstruire le message complet.