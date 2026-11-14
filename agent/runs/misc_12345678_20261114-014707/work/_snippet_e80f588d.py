import base64

# Le payload complet décodé
payload = b'\x8fH\xf4\xbf\xdb}\x93I\xf4\xc3\xdb\xbd\x97It\xcb\xdb=\x8bJ4,\x84\x93 \xd1N $C2_5t3@1_\xaa\xc4\xc3D2_5t3@1_'

# La clé est \xaa\xc4\xc3D (4 octets)
key = b'\xaa\xc4\xc3D'

# Extrait la partie binaire (avant le premier '2_5t3@1_')
# Trouvons la position de '2_5t3@1_'
marker = b'2_5t3@1_'
pos = payload.find(marker)
print(f"Position du premier '2_5t3@1_': {pos}")

binary_part = payload[:pos]
print(f"Longueur de la partie binaire: {len(binary_part)}")
print(f"Hex de la partie binaire: {binary_part.hex()}")

# Essayons de XORer la partie binaire avec la clé répétée
def xor_with_key(data, key):
    result = bytearray()
    for i, b in enumerate(data):
        result.append(b ^ key[i % len(key)])
    return bytes(result)

decoded = xor_with_key(binary_part, key)
print(f"Décodage XOR avec clé: {repr(decoded)}")

# Vérifions si ça commence par 'csaw{'
if decoded.startswith(b'csaw{'):
    print("TROUVÉ! Le flag est:", decoded.decode('ascii', errors='replace'))
else:
    # Peut-être que la clé est différente
    # Essayons avec 'qsTDRC' décodé en Base64
    key2 = base64.b64decode('qsTDRC' + '==')  # Padding
    print(f"Clé 'qsTDRC' décodée: {key2.hex()}")
    decoded2 = xor_with_key(binary_part, key2)
    print(f"Décodage avec clé2: {repr(decoded2)}")