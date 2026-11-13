import wave

# Lire le fichier WAV
with wave.open('audio.wav', 'rb') as wav:
    data = wav.readframes(wav.getnframes())

# Extraire tous les bits LSB
lsb_bits = [byte & 1 for byte in data]

# Convertir en bytes
def bits_to_bytes(bits, start=0):
    result = []
    for i in range(start, len(bits) - 7, 8):
        byte_val = int(''.join(map(str, bits[i:i+8])), 2)
        result.append(byte_val)
    return bytes(result)

# Essayer XOR avec "12345678" sur les bytes LSB
lsb_bytes = bits_to_bytes(lsb_bits)
key = b"12345678"

# XOR avec la clé répétée
xored = bytes([b ^ key[i % len(key)] for i, b in enumerate(lsb_bytes)])

# Chercher "csaw{" dans le résultat XOR
text_xored = ''.join(chr(b) if 32 <= b < 127 else '.' for b in xored)
idx = text_xored.find('csaw{')
if idx != -1:
    print(f"Trouvé 'csaw{{' à l'index byte {idx}")
    print(f"Flag potentiel: {text_xored[idx:idx+50]}")
else:
    print("Pas trouvé avec XOR direct")
    # Chercher "{"
    idx_brace = text_xored.find('{')
    if idx_brace != -1:
        print(f"'{'{' }' trouvé à {idx_brace}")
        print(f"Contexte: {text_xored[max(0, idx_brace-10):idx_brace+50]}")

# Peut-être que le XOR commence à un offset spécifique
# Essayons différents offsets
print("\n--- Recherche avec différents offsets ---")
for offset in [0, 1121, 1121 // 8, 140, 1000, 5000]:
    xored_offset = bytes([b ^ key[(i + offset) % len(key)] for i, b in enumerate(lsb_bytes)])
    text_offset = ''.join(chr(b) if 32 <= b < 127 else '.' for b in xored_offset)
    idx = text_offset.find('csaw{')
    if idx != -1:
        print(f"Offset {offset}: Trouvé à {idx}")
        print(f"Flag: {text_offset[idx:idx+60]}")
        break
else:
    print("Aucun offset trouvé")
