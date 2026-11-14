# Le payload binaire est: \x8fH\xf4\xbf\xdb}\x93I\xf4\xc3\xdb\xbd\x97It\xcb\xdb=\x8bJ4,\x84\x93 \xd1N $C
# C'est 30 octets.

# Peut-être que ces 30 octets sont le flag XORé avec 'qsTDRC' répété.
# Ou peut-être que c'est le flag XORé avec '2_5t3@1_' répété.

binary = b'\x8fH\xf4\xbf\xdb}\x93I\xf4\xc3\xdb\xbd\x97It\xcb\xdb=\x8bJ4,\x84\x93 \xd1N $C'

# Clé 1: qsTDRC décodé en Base64 = \xaa\xc4\xc3D
key1 = b'\xaa\xc4\xc3D'

# Clé 2: 2_5t3@1_
key2 = b'2_5t3@1_'

# Clé 3: qsTDRC en ASCII
key3 = b'qsTDRC'

def xor_with_key(data, key):
    result = bytearray()
    for i, b in enumerate(data):
        result.append(b ^ key[i % len(key)])
    return bytes(result)

print("XOR avec key1 (qsTDRC décodé):")
result1 = xor_with_key(binary, key1)
print(repr(result1))
print("En ASCII:", result1.decode('ascii', errors='replace'))

print("\nXOR avec key2 (2_5t3@1_):")
result2 = xor_with_key(binary, key2)
print(repr(result2))
print("En ASCII:", result2.decode('ascii', errors='replace'))

print("\nXOR avec key3 (qsTDRC ASCII):")
result3 = xor_with_key(binary, key3)
print(repr(result3))
print("En ASCII:", result3.decode('ascii', errors='replace'))

# Peut-être que le flag est 'csaw{' + quelque chose
# Si le flag commence par 'csaw{', alors les 5 premiers octets XORés devraient donner 'csaw{'
print("\n---")
print("Si le flag commence par 'csaw{', quelle clé donnerait ça?")
target = b'csaw{'
# Les 5 premiers octets du binary XORés avec la clé devraient donner 'csaw{'
# Donc clé[i] = binary[i] XOR target[i]
derived_key = bytes([binary[i] ^ target[i] for i in range(5)])
print(f"Clé dérivée pour obtenir 'csaw{'}': {derived_key.hex()}")
print(f"Clé dérivée en ASCII: {derived_key.decode('ascii', errors='replace')}")