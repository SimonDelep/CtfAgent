import wave
import struct

# Ouvrir le fichier WAV
with wave.open('audio.wav', 'rb') as wav:
    data = wav.readframes(wav.getnframes())
    
# Convertir en échantillons 16-bit stéréo
samples = struct.unpack('<' + 'h' * (len(data) // 2), data)

# Essayer de voir si les valeurs absolues ou les différences contiennent des caractères
# Regardons les valeurs non nulles
non_zero = [s for s in samples if s != 0]
print(f"Nombre de valeurs non nulles: {len(non_zero)}")
print(f"Valeurs non nulles (premières 100): {non_zero[:100]}")

# Vérifier si certaines valeurs correspondent à des caractères ASCII imprimables
ascii_chars = []
for s in samples:
    if 32 <= abs(s) <= 126:
        ascii_chars.append(chr(abs(s)))
    elif s == 0:
        ascii_chars.append(' ')

# Afficher la première partie
print(f"Premiers 200 caractères potentiels: {''.join(ascii_chars[:200])}")