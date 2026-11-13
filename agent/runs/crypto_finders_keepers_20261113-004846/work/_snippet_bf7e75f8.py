import base64

encoded = "ZXNucHtkMGNfQHl6QGdsX21uMGpfcG0zejNfZzBfbzAwc30="
decoded = base64.b64decode(encoded)
print("Décodé:", decoded)

# Essayons de trouver un XOR avec "csaw"
target_prefix = b"csaw{"
observed_prefix = decoded[:5]
print("Observed prefix:", observed_prefix)
print("Target prefix:", target_prefix)

# Calculer la clé XOR
xor_key = bytes([o ^ t for o, t in zip(observed_prefix, target_prefix)])
print("XOR key:", xor_key)

# Appliquer cette clé à tout le message
key = xor_key
result = bytes([b ^ key[i % len(key)] for i, b in enumerate(decoded)])
print("Résultat XOR:", result)