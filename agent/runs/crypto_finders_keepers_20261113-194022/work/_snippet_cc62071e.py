# Le ciphertext après { est: d0c_@yz@gl_mn0j_pm3z3_g0_o00s
# Les lettres sont: d c y z g l m n j p m z g o s (15 lettres)

# Si on veut que le texte clair commence par "you_always", les premières lettres seraient:
# y o u a l w a y s ...

ciph_letters = list("dcyzglmnjpmzgos")  # 15 lettres
# Hypothèse: le texte clair est "you_always_be_here_to_off" ou similaire
# Mais comptons les lettres dans "you_always_be_here_to_off":
# y o u a l w a y s b e h e r e t o o f f = 19 lettres (trop)

# Essayons "you_always_here_to_off":
# y o u a l w a y s h e r e t o o f f = 17 lettres (encore trop)

# Essayons "you_always_be_here":
# y o u a l w a y s b e h e r e = 15 lettres ! Parfait !

plain_guess = list("youalwaystobehere")  # 15 lettres
print("Ciphertext lettres:", ''.join(ciph_letters))
print("Clair supposé:", ''.join(plain_guess))
print("Longueur:", len(ciph_letters), len(plain_guess))

# Calculons la clé nécessaire
key_needed = []
for c, p in zip(ciph_letters, plain_guess):
    base = ord('a')
    shift = (ord(p) - ord(c)) % 26
    key_char = chr(base + shift)
    key_needed.append(key_char)

print("\nClé déduite:", ''.join(key_needed))

# Vérifions avec cette clé
def vigenere_decrypt(ciphertext, key):
    result = []
    key_idx = 0
    for char in ciphertext:
        if char.isalpha():
            base = ord('A') if char.isupper() else ord('a')
            key_char = key[key_idx % len(key)]
            key_shift = ord(key_char.lower()) - ord('a')
            decrypted = chr((ord(char) - base - key_shift) % 26 + base)
            result.append(decrypted)
            key_idx += 1
        else:
            result.append(char)
    return ''.join(result)

test_key = ''.join(key_needed)
print("\nDéchiffré avec la clé déduite:", vigenere_decrypt(ciphertext, test_key))