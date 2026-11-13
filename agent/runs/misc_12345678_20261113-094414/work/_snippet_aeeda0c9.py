import wave
import struct

# Ouvrir le fichier WAV
with wave.open('audio.wav', 'rb') as wav:
    data = wav.readframes(wav.getnframes())
    
# Convertir en échantillons 16-bit stéréo
samples = struct.unpack('<' + 'h' * (len(data) // 2), data)

# Peut-être que le message est dans les valeurs absolues des échantillons
# et qu'il faut les lire comme des caractères ASCII
# Essayons de voir si les valeurs forment "csaw{" ou quelque chose de similaire

# Cherchons la séquence "csaw" dans les valeurs
target = [ord(c) for c in "csaw"]
print(f"Recherche de {target} dans les valeurs absolues")

# Trouver toutes les occurrences de chaque valeur
for i, s in enumerate(samples):
    if abs(s) == ord('c'):
        print(f"Trouvé 'c' à la position {i}, valeur {s}")
    if abs(s) == ord('s'):
        print(f"Trouvé 's' à la position {i}, valeur {s}")
    if abs(s) == ord('a'):
        print(f"Trouvé 'a' à la position {i}, valeur {s}")
    if abs(s) == ord('w'):
        print(f"Trouvé 'w' à la position {i}, valeur {s}")