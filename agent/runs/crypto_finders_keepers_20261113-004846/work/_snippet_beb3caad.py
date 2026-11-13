import base64

encoded = "ZXNucHtkMGNfQHl6QGdsX21uMGpfcG0zejNfZzBfbzAwc30="
decoded = base64.b64decode(encoded).decode('utf-8')
print("Décodé:", decoded)

# Essayons de trouver un motif XOR avec "csaw{"
target = "csaw{"
observed = decoded[:5]

# Calculer les différences
for i, (o, t) in enumerate(zip(observed, target)):
    print(f"{o} ({ord(o)}) -> {t} ({ord(t)}): diff = {ord(t) - ord(o)}, xor = {ord(o) ^ ord(t)}")

# Peut-être que c'est un décalage basé sur la position
print("\nEssai de décalage basé sur la position:")
result = []
for i, c in enumerate(decoded):
    if 'a' <= c <= 'z':
        # Décalage basé sur la position
        shift = i % 26
        new_c = chr((ord(c) - ord('a') + shift) % 26 + ord('a'))
        result.append(new_c)
    elif 'A' <= c <= 'Z':
        shift = i % 26
        new_c = chr((ord(c) - ord('A') + shift) % 26 + ord('A'))
        result.append(new_c)
    else:
        result.append(c)
print("Résultat:", ''.join(result))

# Essai inverse
result2 = []
for i, c in enumerate(decoded):
    if 'a' <= c <= 'z':
        shift = i % 26
        new_c = chr((ord(c) - ord('a') - shift) % 26 + ord('a'))
        result2.append(new_c)
    elif 'A' <= c <= 'Z':
        shift = i % 26
        new_c = chr((ord(c) - ord('A') - shift) % 26 + ord('A'))
        result2.append(new_c)
    else:
        result2.append(c)
print("Résultat inverse:", ''.join(result2))