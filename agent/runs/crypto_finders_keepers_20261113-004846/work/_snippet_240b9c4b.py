import base64

encoded = "ZXNucHtkMGNfQHl6QGdsX21uMGpfcG0zejNfZzBfbzAwc30="
decoded = base64.b64decode(encoded).decode('utf-8')
print("Décodé:", decoded)

# Essayons ROT13
def rot13(s):
    result = []
    for c in s:
        if 'a' <= c <= 'z':
            result.append(chr((ord(c) - ord('a') + 13) % 26 + ord('a')))
        elif 'A' <= c <= 'Z':
            result.append(chr((ord(c) - ord('A') + 13) % 26 + ord('A')))
        else:
            result.append(c)
    return ''.join(result)

print("ROT13:", rot13(decoded))

# Essayons tous les décalages Caesar
for shift in range(26):
    result = []
    for c in decoded:
        if 'a' <= c <= 'z':
            result.append(chr((ord(c) - ord('a') + shift) % 26 + ord('a')))
        elif 'A' <= c <= 'Z':
            result.append(chr((ord(c) - ord('A') + shift) % 26 + ord('A')))
        else:
            result.append(c)
    s = ''.join(result)
    if s.startswith('csaw{'):
        print(f"Shift {shift}: {s}")