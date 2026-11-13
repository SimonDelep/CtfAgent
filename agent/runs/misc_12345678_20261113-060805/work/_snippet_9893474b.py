import wave
import struct

# Ouvrir le fichier wav
with wave.open('audio.wav', 'rb') as wav:
    frames = wav.readframes(wav.getnframes())

# Stéréo, 2 bytes par échantillon
samples = struct.unpack('<' + 'h' * (len(frames) // 2), samples)

# Attends, corrigeons
samples = struct.unpack('<' + 'h' * (len(frames) // 2), frames)

# Séparer les canaux
left = [samples[i] for i in range(0, len(samples), 2)]
right = [samples[i] for i in range(1, len(samples), 2)]

# Peut-être que le message est XORé avec "12345678"
key = "12345678"
key_bytes = [ord(c) for c in key]

# Essayer XOR sur le canal gauche
xor_result = []
for i, s in enumerate(left):
    # Prendre les 8 bits de poids faible et XOR avec la clé
    byte_val = s & 0xFF
    key_byte = key_bytes[i % len(key_bytes)]
    xor_byte = byte_val ^ key_byte
    xor_result.append(xor_byte)

print("XOR avec '12345678' sur canal gauche - premiers 200 bytes:")
result = ''.join(chr(b) if 32 <= b < 127 else '.' for b in xor_result[:200])
print(result)

# Chercher "csaw{"
print("\nRecherche de 'csaw{'...")
for i in range(len(xor_result) - 5):
    chunk = xor_result[i:i+5]
    if chunk == [ord('c'), ord('s'), ord('a'), ord('w'), ord('{')]:
        print(f"Trouvé 'csaw{{' à l'index {i}")
        context = ''.join(chr(xor_result[j]) if 32 <= xor_result[j] < 127 else '.' for j in range(i, min(len(xor_result), i+60)))
        print("Contexte:", context)