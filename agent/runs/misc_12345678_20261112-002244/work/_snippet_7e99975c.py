import wave
import struct

# Lire le fichier WAV
w = wave.open('audio.wav', 'rb')
frames = w.readframes(w.getnframes())
w.close()

# Convertir en samples
samples = struct.unpack('<' + 'h' * (len(frames) // 2), frames)

# Extraire les bits LSB de chaque sample
lsb_bits = [s & 1 for s in samples]

# Regrouper par 8 pour former des bytes
bytes_from_lsb = []
for i in range(0, len(lsb_bits) - 7, 8):
    byte_val = 0
    for j in range(8):
        byte_val |= (lsb_bits[i + j] << j)
    bytes_from_lsb.append(byte_val)

# Essayer de décoder en texte
text = ''.join(chr(b) if 32 <= b < 127 else '?' for b in bytes_from_lsb[:200])
print("LSB décodé (premiers 200 bytes):")
print(text)

# Afficher les bytes bruts
print("\nBytes bruts (premiers 50):", bytes_from_lsb[:50])