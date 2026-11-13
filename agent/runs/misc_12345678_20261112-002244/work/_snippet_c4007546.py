import wave

# Lire le fichier WAV
with wave.open('audio.wav', 'rb') as wav:
    data = wav.readframes(wav.getnframes())

# Extraire tous les bits LSB
lsb_bits = [byte & 1 for byte in data]

# Convertir en bytes (8 bits = 1 byte)
def bits_to_text(bits, start=0, length=None):
    if length is None:
        length = len(bits) - start
    text = ''
    for i in range(start, start + length - 7, 8):
        if i + 8 <= len(bits):
            byte_val = int(''.join(map(str, bits[i:i+8])), 2)
            text += chr(byte_val) if 32 <= byte_val < 127 else '.'
    return text

# Chercher "csaw{" dans le texte LSB brut
text_full = bits_to_text(lsb_bits, 0, min(20000, len(lsb_bits)))
print("Recherche de 'csaw{' dans le texte LSB brut:")
idx = text_full.find('csaw{')
if idx != -1:
    print(f"Trouvé à l'index byte {idx * 8}")
    print(f"Contexte: {text_full[max(0, idx-10):idx+50]}")
else:
    print("Pas trouvé directement")

# Chercher "{" seul
idx_brace = text_full.find('{')
if idx_brace != -1:
    print(f"\n'{'{' }' trouvé à l'index byte {idx_brace * 8}")
    print(f"Contexte: {text_full[max(0, idx_brace-10):idx_brace+50]}")

# Chercher "}" 
idx_close = text_full.find('}')
if idx_close != -1:
    print(f"\n'}}' trouvé à l'index byte {idx_close * 8}")
    print(f"Contexte: {text_full[max(0, idx_close-50):idx_close+10]}")
