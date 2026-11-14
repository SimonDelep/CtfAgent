import base64
import re

# Lire le fichier audio
with open('audio.wav', 'rb') as f:
    data = f.read()

# Extraire toutes les chaînes Base64 potentielles
b64_pattern = re.compile(r'[A-Za-z0-9+/]{4,}={0,2}')
b64_strings = b64_pattern.findall(data.decode('latin-1'))

# Décode chaque chaîne
decoded_parts = []
for s in b64_strings:
    try:
        padded = s + '=' * (4 - len(s) % 4) if len(s) % 4 else s
        decoded = base64.b64decode(padded)
        decoded_parts.append(decoded)
    except:
        pass

full_decoded = b''.join(decoded_parts)

# Afficher le début du flux décodé
print(f"Longueur: {len(full_decoded)}")
print(f"Début du flux (hex): {full_decoded[:50].hex()}")
print(f"Début du flux (repr): {full_decoded[:50]!r}")

# Le flux commence par 'D\x81EX\x05D~k...'
# Essayons de voir si 'csaw{' XORé avec quelque chose donne ça
# 'csaw{' en hex: 63 73 61 77 7b

target = b'csaw{'
print(f"\n'csaw{' en hex: {target.hex()}")

# Si le début du flux est le XOR de 'csaw{' avec une clé, quelle serait la clé?
key_candidate = bytes([full_decoded[i] ^ target[i] for i in range(len(target))])
print(f"Clé candidate (XOR avec 'csaw{{'): {key_candidate!r} (hex: {key_candidate.hex()})")