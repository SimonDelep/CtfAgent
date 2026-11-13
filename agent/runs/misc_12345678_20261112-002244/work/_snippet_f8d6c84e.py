import wave

# Lire le fichier WAV
with wave.open('audio.wav', 'rb') as wav:
    data = wav.readframes(wav.getnframes())

# Séparer les canaux (stéréo 16-bit interleaved)
# Chaque échantillon fait 2 bytes, interleaved L R L R ...
left_samples = data[0::4] + data[1::4]  # Bytes des canaux gauche
right_samples = data[2::4] + data[3::4]  # Bytes des canaux droit

# Extraire LSB de chaque canal
left_lsb = [b & 1 for b in left_samples]
right_lsb = [b & 1 for b in right_samples]

# Convertir en bytes
def bits_to_bytes(bits):
    result = []
    for i in range(0, len(bits) - 7, 8):
        byte_val = int(''.join(map(str, bits[i:i+8])), 2)
        result.append(byte_val)
    return bytes(result)

left_bytes = bits_to_bytes(left_lsb)
right_bytes = bits_to_bytes(right_lsb)

key = b"12345678"

# Appliquer XOR avec la clé sur chaque canal
def xor_with_key(data, key):
    return bytes([b ^ key[i % len(key)] for i, b in enumerate(data)])

left_xored = xor_with_key(left_bytes, key)
right_xored = xor_with_key(right_bytes, key)

# Chercher "csaw{" dans chaque canal XORé
for name, bytes_data in [("Gauche", left_xored), ("Droit", right_xored)]:
    text = ''.join(chr(b) if 32 <= b < 127 else '.' for b in bytes_data)
    idx = text.find('csaw{')
    if idx != -1:
        print(f"\n{name}: 'csaw{{' trouvé à {idx}")
        # Extraire le flag complet (jusqu'à '}')
        end_idx = text.find('}', idx)
        if end_idx != -1:
            print(f"Flag: {text[idx:end_idx+1]}")
        else:
            print(f"Flag potentiel: {text[idx:idx+60]}")
    else:
        # Chercher "{"
        idx_brace = text.find('{')
        if idx_brace != -1:
            print(f"\n{name}: '{'{' }' trouvé à {idx_brace}")
            print(f"Contexte: {text[max(0, idx_brace-10):idx_brace+50]}")

# Peut-être que la clé commence à un offset différent
print("\n--- Recherche avec différents offsets de clé ---")
for offset in range(8):
    left_xored_off = bytes([b ^ key[(i + offset) % len(key)] for i, b in enumerate(left_bytes)])
    right_xored_off = bytes([b ^ key[(i + offset) % len(key)] for i, b in enumerate(right_bytes)])
    
    for name, bytes_data in [("Gauche", left_xored_off), ("Droit", right_xored_off)]:
        text = ''.join(chr(b) if 32 <= b < 127 else '.' for b in bytes_data)
        idx = text.find('csaw{')
        if idx != -1:
            print(f"Offset {offset}, {name}: 'csaw{{' trouvé à {idx}")
            end_idx = text.find('}', idx)
            if end_idx != -1:
                print(f"Flag: {text[idx:end_idx+1]}")
