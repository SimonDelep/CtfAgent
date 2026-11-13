import base64

encoded = "ZXNucHtkMGNfQHl6QGdsX21uMGpfcG0zejNfZzBfbzAwc30="
decoded = base64.b64decode(encoded).decode('utf-8')
print(f"Base64 décodé: {decoded}")

# Comparaison avec csaw{...}
expected_prefix = "csaw{"
actual_prefix = decoded[:5]
print(f"Prefix attendu: {expected_prefix}")
print(f"Prefix réel: {actual_prefix}")

# Différence entre les caractères
for i, (a, b) in enumerate(zip(actual_prefix, expected_prefix)):
    print(f"  {a} -> {b}: diff = {ord(a) - ord(b)}")