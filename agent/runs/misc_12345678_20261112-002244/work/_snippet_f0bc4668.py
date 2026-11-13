import wave

# Lire le fichier WAV
with wave.open('audio.wav', 'rb') as wav:
    data = wav.readframes(wav.getnframes())

# Séparer les canaux
left_samples = data[0::4] + data[1::4]
right_samples = data[2::4] + data[3::4]

# Extraire LSB
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

# Chercher "csaw" dans les bytes bruts (sans XOR)
for name, bytes_data in [("Gauche", left_bytes), ("Droit", right_bytes)]:
    text = ''.join(chr(b) if 32 <= b < 127 else '.' for b in bytes_data)
    idx = text.find('csaw')
    if idx != -1:
        print(f"{name}: 'csaw' trouvé à {idx}")
        print(f"Contexte: {text[idx:idx+50]}")
    else:
        # Chercher "csaw" en cherchant chaque caractère
        for i in range(len(text) - 3):
            if text[i:i+4] == 'csaw':
                print(f"{name}: 'csaw' trouvé à {i}")
                print(f"Contexte: {text[i:i+50]}")
                break

# Peut-être que le flag est dans les données audio elles-mêmes, pas dans les LSB
# Ou peut-être que c'est un encodage différent

# Essayons de chercher "csaw" dans les données brutes du fichier
print("\n--- Recherche dans les données brutes du fichier WAV ---")
with open('audio.wav', 'rb') as f:
    raw_data = f.read()

idx = raw_data.find(b'csaw')
if idx != -1:
    print(f"'csaw' trouvé dans les données brutes à l'offset {idx}")
    print(f"Contexte: {raw_data[idx:idx+50]}")
else:
    print("'csaw' pas trouvé dans les données brutes")

# Chercher "{"
idx = raw_data.find(b'{')
if idx != -1:
    print(f"'{'{' }' trouvé dans les données brutes à l'offset {idx}")
    print(f"Contexte: {raw_data[max(0, idx-10):idx+50]}")
