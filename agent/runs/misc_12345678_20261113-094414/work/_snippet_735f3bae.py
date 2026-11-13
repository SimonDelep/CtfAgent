import wave
import struct

# Ouvrir le fichier WAV
with wave.open('audio.wav', 'rb') as wav:
    data = wav.readframes(wav.getnframes())
    
# Convertir en échantillons 16-bit stéréo
samples = struct.unpack('<' + 'h' * (len(data) // 2), data)

# Peut-être que le message est dans les positions où les valeurs sont exactement certaines valeurs
# Regardons si les valeurs 99, 115, 97, 119 (c, s, a, w) apparaissent dans un ordre spécifique

# Cherchons la séquence "csaw{" en cherchant les positions consécutives
# d'abord, trouvons toutes les positions de chaque caractère
positions_c = [i for i, s in enumerate(samples) if abs(s) == 99]
positions_s = [i for i, s in enumerate(samples) if abs(s) == 115]
positions_a = [i for i, s in enumerate(samples) if abs(s) == 97]
positions_w = [i for i, s in enumerate(samples) if abs(s) == 119]
positions_open = [i for i, s in enumerate(samples) if abs(s) == 123]  # '{'

print(f"Positions de 'c' (99): {len(positions_c)} occurrences")
print(f"Positions de 's' (115): {len(positions_s)} occurrences")
print(f"Positions de 'a' (97): {len(positions_a)} occurrences")
print(f"Positions de 'w' (119): {len(positions_w)} occurrences")
print(f"Positions de '{{' (123): {len(positions_open)} occurrences")

# Peut-être que le message est dans les positions elles-mêmes
# ou dans les différences entre positions