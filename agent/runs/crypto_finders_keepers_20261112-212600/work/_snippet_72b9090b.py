import base64

encoded = "ZXNucHtkMGNfQHl6QGdsX21uMGpfcG0zejNfZzBfbzAwc30="
decoded_bytes = base64.b64decode(encoded)
print("Bytes:", list(decoded_bytes))
print("As string:", decoded_bytes.decode('utf-8'))

# Peut-être que c'est XOR avec quelque chose
target = "csaw{"
for xor_key in range(256):
    result = bytes([b ^ xor_key for b in decoded_bytes[:5]])
    if result.decode('utf-8', errors='ignore') == target:
        print(f"XOR key {xor_key} gives: {result}")