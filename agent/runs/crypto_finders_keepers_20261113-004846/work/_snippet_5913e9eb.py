import base64

encoded = "ZXNucHtkMGNfQHl6QGdsX21uMGpfcG0zejNfZzBfbzAwc30="
decoded = base64.b64decode(encoded).decode('utf-8')
print("Décodage Base64:", decoded)

# C'est bien "esnp{d0c_@yz@gl_mn0j_pm3z3_g0_o00s}"
# Maintenant, comment transformer "esnp" en "csaw" ?

# e -> c : -2
# s -> s : 0
# n -> a : -13
# p -> w : +7

# Peut-être que c'est un décalage basé sur la position ?
# Ou une clé XOR qui est un mot spécifique

# Essayons de voir si c'est un XOR avec une clé qui est "csaw" répété
cipher = decoded
key = "csaw"
result = []
for i, c in enumerate(cipher):
    result.append(chr(ord(c) ^ ord(key[i % len(key)])))
print("XOR avec 'csaw':", ''.join(result))

# Ou peut-être que la clé est différente
# Regardons les différences entre cipher et plain pour trouver la clé

plain = "csaw{"
for i in range(len(plain)):
    diff = ord(cipher[i]) ^ ord(plain[i])
    print(f"Position {i}: {cipher[i]} XOR {plain[i]} = {diff} ({chr(diff) if 32 <= diff < 127 else '?'})")
