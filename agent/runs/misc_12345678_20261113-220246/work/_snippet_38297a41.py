import base64

# Le flux décodé complet
full_decoded = bytes.fromhex('4481455805447e6b179039bb6ab65fe5beab6ab667e5fea7fa3fe7ce48cf9cf9139079f5af4ad09dd3bd3bebee83139039d5eda1d80b4174d33e71e73dd58d74b7dbbd9f49f4bfdc3d9749b4c7dbfd9749b4bfdc7d9348f4c3db7d8f49b4b7db3d9749f4c3dc3d8f48f4bfdb7d9349f4c3dbbd974974cbdb3d8b4a342c849320d14e202443325f35743340315faac4c344325f35743340315f')

# La clé potentielle: qsTDRC décodé = \xaa\xc4\xc3D
key = bytes.fromhex('aac4c344')
print(f"Clé (qsTDRC décodé): {key} (hex: {key.hex()})")

# Essayer de XORer le flux avec la clé
xored = bytes([b ^ key[i % len(key)] for i, b in enumerate(full_decoded)])
print(f"XOR avec clé: {xored}")
print(f"XOR (hex): {xored.hex()}")

# Chercher 'csaw{' dans le résultat
if b'csaw{' in xored:
    print("Trouvé 'csaw{' dans le XOR!")
else:
    print("'csaw{' non trouvé dans le XOR")

# Essayer aussi avec '2_5t3@1_' comme clé
key2 = b'2_5t3@1_'
xored2 = bytes([b ^ key2[i % len(key2)] for i, b in enumerate(full_decoded)])
print(f"\nXOR avec '2_5t3@1_': {xored2}")
if b'csaw{' in xored2:
    print("Trouvé 'csaw{' dans le XOR avec 2_5t3@1_!")