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

lsb_bytes = bits_to_bytes(lsb_bits)

# Peut-être que le flag n'est pas XORé avec "12345678" mais que "12345678" est le flag lui-même?
# Ou peut-être que c'est un autre type d'encodage

# Essayons de chercher des motifs dans les bytes LSB bruts
print("Recherche de motifs dans les bytes LSB bruts:")
text_raw = ''.join(chr(b) if 32 <= b < 127 else '.' for b in lsb_bytes)

# Chercher "csaw"
idx = text_raw.find('csaw')
if idx != -1:
    print(f"'csaw' trouvé à l'index {idx}")
    print(f"Contexte: {text_raw[idx:idx+50]}")
else:
    print("'csaw' pas trouvé en brut")

# Chercher "{"
idx = text_raw.find('{')
if idx != -1:
    print(f"'{'{' }' trouvé à l'index {idx}")
    print(f"Contexte: {text_raw[max(0, idx-10):idx+50]}")

# Peut-être que le flag est encodé en binaire et qu'il faut le lire différemment
# Ou peut-être que c'est dans un canal spécifique (gauche ou droit)

# Le fichier est stéréo - séparons les canaux
print("\n--- Séparation des canaux ---")
# Pour un fichier stéréo 16-bit, les échantillons sont interleaved: L R L R ...
# Chaque échantillon fait 2 bytes

with wave.open('audio.wav', 'rb') as wav:
    data = wav.readframes(wav.getnframes())

# data est interleaved: byte0, byte1 (L), byte2, byte3 (R), etc.
# Pour 16-bit, chaque échantillon est 2 bytes
samples = len(data) // 2
left_samples = data[0::4] + data[1::4]  # Bytes des canaux gauche
right_samples = data[2::4] + data[3::4]  # Bytes des canaux droit

print(f"Nombre d'échantillons par canal: {samples // 2}")

# Extraire LSB de chaque canal séparément
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

# Chercher "csaw{" dans chaque canal
for name, bytes_data in [("Gauche", left_bytes), ("Droit", right_bytes)]:
    text = ''.join(chr(b) if 32 <= b < 127 else '.' for b in bytes_data)
    idx = text.find('csaw{')
    if idx != -1:
        print(f"\n{name}: 'csaw{{' trouvé à {idx}")
        print(f"Flag: {text[idx:idx+60]}")
    else:
        idx_brace = text.find('{')
        if idx_brace != -1:
            print(f"\n{name}: '{'{' }' trouvé à {idx_brace}")
            print(f"Contexte: {text[max(0, idx_brace-10):idx_brace+50]}")
