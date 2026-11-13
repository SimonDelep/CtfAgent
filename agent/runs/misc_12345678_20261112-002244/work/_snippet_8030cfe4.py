import wave
import struct

# Lire le fichier WAV
w = wave.open('audio.wav', 'rb')
frames = w.readframes(w.getnframes())
w.close()

samples = struct.unpack('<' + 'h' * (len(frames) // 2), frames)

# Essayer de convertir les samples en texte directement
# Peut-être que les valeurs des samples correspondent à des codes ASCII

# Regardons les valeurs uniques et leur distribution
unique_vals = set(samples)
print(f"Nombre de valeurs uniques: {len(unique_vals)}")

# Cherchons si certaines valeurs apparaissent souvent
from collections import Counter
counter = Counter(samples)
most_common = counter.most_common(20)
print("Valeurs les plus fréquentes:", most_common)

# Peut-être que le flag est encodé en utilisant seulement certaines valeurs
# Essayons de mapper les valeurs à des caractères

# Une autre idée: le titre "12345678" pourrait indiquer qu'il faut prendre
# chaque 8ème sample ou quelque chose comme ça

# Essayons de prendre chaque 8ème sample et voir si ça donne un texte
every_8th = samples[::8]
print("\nTous les 8èmes samples (premiers 50):", every_8th[:50])

# Convertir en texte si possible
text_8th = ''.join(chr(abs(s) % 128) if 32 <= abs(s) % 128 < 127 else '.' for s in every_8th[:200])
print("Texte décodé:", text_8th)