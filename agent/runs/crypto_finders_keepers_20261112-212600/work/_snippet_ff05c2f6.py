import base64

encoded = "ZXNucHtkMGNfQHl6QGdsX21uMGpfcG0zejNfZzBfbzAwc30="
decoded = base64.b64decode(encoded).decode('utf-8')
print("Decoded:", decoded)

# Essayons de trouver un pattern XOR répétitif
# On suppose que le flag est de la forme "csaw{...}"
# Donc les premiers caractères sont "csaw{"

# Si on XOR avec "csaw{csaw{..."
target_pattern = "csaw{"
key_bytes = []
for i, c in enumerate(decoded):
    t = target_pattern[i % len(target_pattern)]
    key_bytes.append(ord(c) ^ ord(t))

print("Key bytes:", key_bytes)
print("Key as hex:", ' '.join(f'{k:02x}' for k in key_bytes))

# Peut-être que la clé est "csaw" répété
# Regardons si XOR avec "csaw" donne quelque chose de lisible
key_str = "csaw"
result = ""
for i, c in enumerate(decoded):
    if c.isalpha():
        k = ord(key_str[i % len(key_str)])
        result += chr(ord(c) ^ k)
    else:
        result += c
print("XOR avec 'csaw':", result)

# Essayons avec la clé trouvée
# Peut-être que la clé est "flag" ou autre
for test_key in ["flag", "key", "secret", "hidden", "csaw", "finders"]:
    result = ""
    for i, c in enumerate(decoded):
        if c.isalpha():
            k = ord(test_key[i % len(test_key)])
            result += chr(ord(c) ^ k)
        else:
            result += c
    print(f"XOR avec '{test_key}': {result}")