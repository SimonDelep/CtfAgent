import wave
import struct
import numpy as np

# Lire le fichier WAV
w = wave.open('audio.wav', 'rb')
frames = w.readframes(w.getnframes())
w.close()

samples = struct.unpack('<' + 'h' * (len(frames) // 2), frames)

# Convertir en numpy array
data = np.array(samples, dtype=np.int16)

# Essayer de trouver des motifs répétitifs ou des séquences spécifiques
# Peut-être que le flag est encodé en Morse ou autre

# Vérifier si les samples contiennent des valeurs spécifiques
# Cherchons des séquences de valeurs qui pourraient correspondre à des caractères ASCII

# Une autre approche: regarder les différences entre samples consécutifs
diffs = np.diff(data)
print("Différences min/max:", diffs.min(), diffs.max())

# Peut-être que le flag est dans les valeurs absolues ou quelque chose comme ça
# Essayons de convertir les samples en bytes directement (prendre le byte de poids faible)
low_bytes = [s & 0xFF for s in samples]
high_bytes = [(s >> 8) & 0xFF for s in samples]

print("\nLow bytes (premiers 50):", low_bytes[:50])
print("\nHigh bytes (premiers 50):", high_bytes[:50])

# Essayer de décoder les low bytes comme texte
text_low = ''.join(chr(b) if 32 <= b < 127 else '.' for b in low_bytes[:200])
print("\nLow bytes texte:", text_low)