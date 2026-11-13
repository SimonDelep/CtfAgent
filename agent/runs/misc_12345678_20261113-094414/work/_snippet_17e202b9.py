import wave
import struct

# Ouvrir le fichier WAV
with wave.open('audio.wav', 'rb') as wav:
    data = wav.readframes(wav.getnframes())
    
# Convertir en échantillons 16-bit stéréo
samples = struct.unpack('<' + 'h' * (len(data) // 2), data)

# Extraire les bits LSB de chaque échantillon
lsb_bits = [s & 1 for s in samples]

# Regrouper par 8 bits pour former des octets
bytes_from_lsb = []
for i in range(0, len(lsb_bits) - 7, 8):
    byte_val = 0
    for j in range(8):
        byte_val |= (lsb_bits[i + j] << j)
    bytes_from_lsb.append(byte_val)

# Essayer de décoder comme ASCII
try:
    text = bytes(bytes_from_lsb).decode('ascii', errors='ignore')
    print(f"Longueur du texte: {len(text)}")
    print(f"Texte (premières 500 chars): {text[:500]}")
except:
    print("Décodage ASCII échoué")

# Afficher les premiers octets
print(f"Premiers 50 octets LSB: {bytes_from_lsb[:50]}")