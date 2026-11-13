import base64

encoded = "ZXNucHtkMGNfQHl6QGdsX21uMGpfcG0zejNfZzBfbzAwc30="
decoded = base64.b64decode(encoded)
print("Bytes:", decoded)
print("As string:", decoded.decode('utf-8'))

# Peut-être que c'est du base64 inversé ou quelque chose comme ça
# Ou peut-être que c'est un XOR avec une clé simple

# Essayons XOR avec chaque byte de 0 à 255
for key in range(256):
    result = bytes([b ^ key for b in decoded])
    try:
        s = result.decode('utf-8')
        if s.startswith('csaw{'):
            print(f"XOR key {key}: {s}")
    except:
        pass

# Essayons aussi avec une clé de 2 bytes
for k1 in range(256):
    for k2 in range(256):
        result = bytes([b ^ (k1 if i % 2 == 0 else k2) for i, b in enumerate(decoded)])
        try:
            s = result.decode('utf-8')
            if s.startswith('csaw{'):
                print(f"XOR key ({k1}, {k2}): {s}")
        except:
            pass