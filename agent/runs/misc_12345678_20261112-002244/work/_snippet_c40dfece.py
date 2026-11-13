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

# Combiner les LSB (gauche XOR droit ou concaténation)
# Essayons concaténation: L R L R ...
combined_lsb = []
for l, r in zip(left_lsb, right_lsb):
    combined_lsb.append(l)
    combined_lsb.append(r)

# Convertir en bytes
def bits_to_bytes(bits):
    result = []
    for i in range(0, len(bits) - 7, 8):
        byte_val = int(''.join(map(str, bits[i:i+8])), 2)
        result.append(byte_val)
    return bytes(result)

combined_bytes = bits_to_bytes(combined_lsb)

# Chercher "{" dans le combiné
text = ''.join(chr(b) if 32 <= b < 127 else '.' for b in combined_bytes)
idx = text.find('{')
if idx != -1:
    print(f"'{'{' }' trouvé à {idx} dans le combiné")
    print(f"Contexte: {text[max(0, idx-20):idx+50]}")

# Maintenant, essayons de trouver la clé XOR en supposant que le flag commence par "csaw{"
# Si on trouve "{" à l'index idx, alors "csaw{" devrait être à idx-4 à idx+1
# Donc les 5 bytes avant "{" devraient être "csaw" après XOR

# Trouver toutes les occurrences de "{" et essayer de déduire la clé
print("\n--- Recherche de la clé XOR ---")
for start_idx in range(min(1000, len(combined_bytes) - 10)):
    # Supposons que le flag commence à start_idx
    # Les 5 bytes devraient être "csaw{"
    target = b"csaw{"
    candidate_bytes = combined_bytes[start_idx:start_idx+5]
    
    if len(candidate_bytes) < 5:
        continue
    
    # Déduire la clé
    key_candidate = bytes([candidate_bytes[i] ^ target[i] for i in range(5)])
    
    # Vérifier si cette clé donne un flag valide
    # Appliquer la clé sur une plus grande zone
    key_len = 8  # "12345678" fait 8 chars
    xored = bytes([combined_bytes[start_idx + i] ^ key_candidate[i % len(key_candidate)] for i in range(50)])
    xored_text = ''.join(chr(b) if 32 <= b < 127 else '.' for b in xored)
    
    if xored_text.startswith('csaw{') and '}' in xored_text:
        print(f"Clé trouvée: {key_candidate}")
        print(f"Flag potentiel: {xored_text}")
        break

# Peut-être que la clé est "12345678" mais appliquée à partir d'un offset spécifique
print("\n--- Essai avec clé '12345678' à différents offsets ---")
key = b"12345678"
for offset in range(len(combined_bytes) - 100):
    xored = bytes([combined_bytes[offset + i] ^ key[i % len(key)] for i in range(100)])
    xored_text = ''.join(chr(b) if 32 <= b < 127 else '.' for b in xored)
    if xored_text.startswith('csaw{'):
        print(f"Offset {offset}: Flag trouvé!")
        end_idx = xored_text.find('}')
        if end_idx != -1:
            print(f"Flag: {xored_text[:end_idx+1]}")
        break
else:
    print("Aucun offset trouvé avec clé '12345678'")
