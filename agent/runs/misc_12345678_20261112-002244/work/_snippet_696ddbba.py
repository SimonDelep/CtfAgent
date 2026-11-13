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
key = b"12345678"

# XOR avec la clé
xored = bytes([b ^ key[i % len(key)] for i, b in enumerate(lsb_bytes)])

# Regarder autour de l'index 107 où on a trouvé '{'
print("Autour de l'index 107 (où '{' a été trouvé):")
start = max(0, 107 - 20)
end = min(len(xored), 107 + 30)
for i in range(start, end):
    b = xored[i]
    c = chr(b) if 32 <= b < 127 else f'[{b}]'
    print(f"  {i}: {b:3d} = {c}")

# Peut-être que le flag commence avant le '{'
# Cherchons ce qui pourrait être "csaw" avant le '{'
print("\n--- Vérifions si 'csaw' est XORé différemment ---")
# Si '{' est à l'index 107, alors '}' serait à la fin du flag
# Essayons de deviner la clé en supposant que '{' devrait être '{' (déjà XORé)
# Ou peut-être que '{' est le résultat du XOR, donc le byte original XORé avec clé donne '{'

# Byte de '{' = 123
# Si le byte LSB original XOR clé = 123, alors byte LSB original = 123 XOR clé
# Mais on a déjà XORé, donc xored[107] devrait être '{' si c'est correct

print(f"Valeur à l'index 107 après XOR: {xored[107]} = '{chr(xored[107])}'")

# Peut-être que la clé n'est pas "12345678" mais quelque chose d'autre
# Essayons de trouver la clé en supposant que le texte avant '{' est "csaw"
# Si xored[103:107] devrait être "csaw", alors:
# clé[i] = lsb_bytes[103+i] XOR ord('c') etc.

print("\n--- Déduire la clé en supposant 'csaw{' ---")
target = b"csaw{"
for i in range(5):
    if 107 - 5 + i < len(lsb_bytes):
        original_byte = lsb_bytes[107 - 5 + i]
        target_byte = target[i]
        derived_key = original_byte ^ target_byte
        print(f"Position {107-5+i}: LSB={original_byte}, cible='{chr(target_byte)}', clé déduite={derived_key} ('{chr(derived_key) if 32<=derived_key<127 else '?'}')")
