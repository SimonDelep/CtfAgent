import wave
import struct

# Ouvrir le fichier WAV
with wave.open('audio.wav', 'rb') as wav:
    data = wav.readframes(wav.getnframes())
    
# Convertir en échantillons 16-bit stéréo
samples = struct.unpack('<' + 'h' * (len(data) // 2), data)

# Regardons les valeurs qui sont dans la plage ASCII imprimable (32-126)
# et voyons si elles forment un motif
ascii_samples = [(i, s) for i, s in enumerate(samples) if 32 <= abs(s) <= 126]
print(f"Nombre d'échantillons dans la plage ASCII: {len(ascii_samples)}")

# Afficher les positions et valeurs
print("Positions et valeurs (premières 50):")
for pos, val in ascii_samples[:50]:
    print(f"  Position {pos}: valeur {val} -> chr({abs(val)}) = '{chr(abs(val))}'")

# Essayons de voir si les positions elles-mêmes contiennent un message
# ou si les valeurs forment un message quand on les lit dans l'ordre
ascii_chars = [chr(abs(s)) for i, s in enumerate(samples) if 32 <= abs(s) <= 126]
print(f"\nSéquence de caractères ASCII (premières 200): {''.join(ascii_chars[:200])}")