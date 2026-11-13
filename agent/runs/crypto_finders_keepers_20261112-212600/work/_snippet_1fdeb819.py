import base64

encoded = "ZXNucHtkMGNfQHl6QGdsX21uMGpfcG0zejNfZzBfbzAwc30="
decoded = base64.b64decode(encoded).decode('utf-8')
print("Decoded:", decoded)

# Comparons caractère par caractère avec "csaw{...}"
target_start = "csaw{"
for i, (c, t) in enumerate(zip(decoded, target_start)):
    diff = ord(c) - ord(t)
    print(f"Pos {i}: '{c}' ({ord(c)}) vs '{t}' ({ord(t)}) -> diff = {diff}")

# Peut-être que le pattern est différent. Regardons si c'est un décalage de -2 pour certaines positions
# e -> c = -2, s -> s = 0, n -> a = -13, p -> w = +7

# Essayons de décoder avec un décalage différent pour chaque position
# Si on suppose que le flag commence par "csaw{"
# e(101) -> c(99): -2
# s(115) -> s(115): 0
# n(110) -> a(97): -13
# p(112) -> w(119): +7

# Peut-être que c'est un XOR avec une clé répétitive
key = "csaw"
for xor_key in range(256):
    result = ""
    for i, c in enumerate(decoded):
        if c.isalpha():
            k = ord(key[i % len(key)])
            result += chr(ord(c) ^ k)
        else:
            result += c
    if result.startswith("csaw{"):
        print(f"XOR avec clé '{key}': {result}")