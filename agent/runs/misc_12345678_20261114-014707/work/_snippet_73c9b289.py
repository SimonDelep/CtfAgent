import base64
import re

# Lire le fichier WAV
with open('audio.wav', 'rb') as f:
    data = f.read()

# Extraire toutes les chaînes Base64
b64_pattern = re.compile(r'[A-Za-z0-9+/]{4,}={0,2}')
matches = b64_pattern.findall(data.decode('latin-1'))

# Décode chaque chaîne et concaténer
full_payload = b''
for m in matches:
    try:
        padded = m + '=' * (4 - len(m) % 4) if len(m) % 4 else m
        decoded = base64.b64decode(padded)
        full_payload += decoded
    except:
        pass

print(f"Longueur du payload décodé: {len(full_payload)} octets")
print(f"Payload hex (premier 100 octets): {full_payload[:100].hex()}")
print(f"Payload hex (dernier 50 octets): {full_payload[-50:].hex()}")

# Identifier la structure
# On sait que la fin contient: 2_5t3@1_ + \xaa\xc4\xc3D + 2_5t3@1_
# Cherchons ces patterns
text_marker = b'2_5t3@1_'
key_bytes = bytes([0xaa, 0xc4, 0xc3, 0x44])  # qsTDRC décodé

# Trouver les positions
pos1 = full_payload.find(text_marker)
print(f"\nPosition de '2_5t3@1_': {pos1}")

# Chercher le pattern binaire
pos_key = full_payload.find(key_bytes)
print(f"Position de la clé \\xaa\\xc4\\xc3D: {pos_key}")

# Trouver la deuxième occurrence de text_marker
pos2 = full_payload.find(text_marker, pos1 + len(text_marker))
print(f"Deuxième occurrence de '2_5t3@1_': {pos2}")

# Le ciphertext serait avant la première occurrence de text_marker
if pos1 > 0:
    ciphertext = full_payload[:pos1]
    print(f"\nCiphertext (avant premier marker): {len(ciphertext)} octets")
    print(f"Ciphertext hex: {ciphertext.hex()}")
    
    # Essayer XOR avec différentes clés
    # Clé 1: qsTDRC en ASCII
    key_ascii = b'qsTDRC'
    xor_result1 = bytes([c ^ key_ascii[i % len(key_ascii)] for i, c in enumerate(ciphertext)])
    print(f"\nXOR avec 'qsTDRC' (ASCII): {xor_result1}")
    
    # Clé 2: qsTDRC décodé (4 octets)
    xor_result2 = bytes([c ^ key_bytes[i % len(key_bytes)] for i, c in enumerate(ciphertext)])
    print(f"XOR avec clé décodée (4 octets): {xor_result2}")
    
    # Clé 3: 2_5t3@1_ en ASCII
    key_text = b'2_5t3@1_'
    xor_result3 = bytes([c ^ key_text[i % len(key_text)] for i, c in enumerate(ciphertext)])
    print(f"XOR avec '2_5t3@1_' (ASCII): {xor_result3}")