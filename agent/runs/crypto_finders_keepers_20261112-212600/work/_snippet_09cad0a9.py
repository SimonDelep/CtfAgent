import base64

encoded = "ZXNucHtkMGNfQHl6QGdsX21uMGpfcG0zejNfZzBfbzAwc30="
decoded = base64.b64decode(encoded).decode('utf-8')
print("Decoded:", decoded)

# ROT13
def rot13(s):
    result = ""
    for c in s:
        if c.isalpha():
            base = ord('a') if c.islower() else ord('A')
            result += chr((ord(c) - base + 13) % 26 + base)
        else:
            result += c
    return result

print("ROT13:", rot13(decoded))

# Peut-être que c'est un décalage de -2 seulement pour les premières lettres
# e -> c (-2), s -> s (0), n -> a (-13), p -> w (+7)

# Essayons de voir si c'est un chiffrement affine
# Pour e(4) -> c(2): 4*a + b = 2 mod 26
# Pour s(18) -> s(18): 18*a + b = 18 mod 26

# De la deuxième équation: 18a + b = 18 => b = 18 - 18a
# Substituons dans la première: 4a + (18 - 18a) = 2 => -14a = -16 => 14a = 16 => a = 16/14 = 8/7

# Ce n'est pas simple. Essayons autre chose.

# Peut-être que le flag est juste le texte décodé mais avec un décalage différent
# Regardons si "esnp" pourrait être "csaw" avec un décalage de -2 pour e->c
# Mais s->s est 0, n->a est -13...

# Attends, peut-être que c'est un décalage basé sur la position
# Position 0: e -> c = -2
# Position 1: s -> s = 0
# Position 2: n -> a = -13
# Position 3: p -> w = +7

# Les différences: -2, 0, -13, +7
# Peut-être que c'est un XOR avec une clé

# Essayons de trouver la clé XOR
target = "csaw{"
key = []
for i, (c, t) in enumerate(zip(decoded, target)):
    key.append(ord(c) ^ ord(t))
print("XOR key bytes:", key)
print("XOR key as chars:", ''.join(chr(k) if 32 <= k < 127 else '?' for k in key))