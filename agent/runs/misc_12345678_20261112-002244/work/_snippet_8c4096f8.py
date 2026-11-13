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

# Peut-être que "12345678" signifie qu'il faut extraire 8 bits LSB (pas juste 1 bit)
# Ou peut-être que c'est un motif de lecture

# Essayons d'extraire 8 bits LSB de chaque byte (c'est ce qu'on a déjà fait)
# Mais peut-être que le motif est différent

# Autre idée: "12345678" pourrait être les valeurs attendues pour les 8 premiers bytes
# Ou peut-être que c'est un décalage de 1, 2, 3, 4, 5, 6, 7, 8 bits

# Essayons de lire les bits LSB avec différents décalages
def extract_bits_with_offset(bits, offset, num_bits=8):
    """Extraire num_bits en commençant à l'offset"""
    result = []
    for i in range(0, len(bits) - offset - num_bits, num_bits):
        byte_val = int(''.join(map(str, bits[i+offset:i+offset+num_bits])), 2)
        result.append(byte_val)
    return bytes(result)

# Essayer différents offsets
print("Essai avec différents offsets de lecture:")
for offset in range(8):
    left_bytes = extract_bits_with_offset(left_lsb, offset)
    right_bytes = extract_bits_with_offset(right_lsb, offset)
    
    for name, bytes_data in [("Gauche", left_bytes), ("Droit", right_bytes)]:
        text = ''.join(chr(b) if 32 <= b < 127 else '.' for b in bytes_data)
        idx = text.find('csaw{')
        if idx != -1:
            print(f"Offset {offset}, {name}: 'csaw{{' trouvé à {idx}")
            end_idx = text.find('}', idx)
            if end_idx != -1:
                print(f"Flag: {text[idx:end_idx+1]}")

# Peut-être que le flag est dans les deux canaux combinés d'une manière spécifique
# Ou peut-être que c'est XOR entre les deux canaux

print("\n--- XOR entre canaux gauche et droit ---")
# XOR des bits LSB des deux canaux
combined_lsb = [l ^ r for l, r in zip(left_lsb, right_lsb)]
combined_bytes = extract_bits_with_offset(combined_lsb, 0)

text = ''.join(chr(b) if 32 <= b < 127 else '.' for b in combined_bytes)
idx = text.find('csaw{')
if idx != -1:
    print(f"XOR canaux: 'csaw{{' trouvé à {idx}")
    end_idx = text.find('}', idx)
    if end_idx != -1:
        print(f"Flag: {text[idx:end_idx+1]}")
else:
    idx_brace = text.find('{')
    if idx_brace != -1:
        print(f"XOR canaux: '{'{' }' trouvé à {idx_brace}")
        print(f"Contexte: {text[max(0, idx_brace-10):idx_brace+50]}")
