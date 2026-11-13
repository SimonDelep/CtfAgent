decoded = "esnp{d0c_@yz@gl_mn0j_pm3z3_g0_o00s}"

# Si le flag attendu est "csaw{...}", alors:
# e -> c (décalage -2)
# s -> s (décalage 0)
# n -> a (décalage -13 ou +13)
# p -> w (décalage +7)

# Peut-être que la clé est "csaw" et que c'est un décalage de Vigenère?
# En Vigenère, pour décoder: plaintext = (ciphertext - key) mod 26

# Essayons de trouver la clé en supposant que le plaintext est "csaw{"
ciphertext = decoded[:5]
expected = "csaw{"

# Pour les lettres seulement
key_chars = []
for c, e in zip(ciphertext, expected):
    if c.isalpha() and e.isalpha():
        c_val = ord(c.lower()) - ord('a')
        e_val = ord(e.lower()) - ord('a')
        # En Vigenère: ciphertext = (plaintext + key) mod 26
        # Donc: key = (ciphertext - plaintext) mod 26
        key_val = (c_val - e_val) % 26
        key_chars.append(chr(key_val + ord('a')))
    else:
        key_chars.append(c)

print(f"Clé déduite: {''.join(key_chars)}")

# Maintenant appliquons cette clé à tout le message
# Mais d'abord, vérifions si la clé est "csaw" ou quelque chose de similaire
# e - c = 4 - 2 = 2 (c)
# s - s = 18 - 18 = 0 (a)
# n - a = 13 - 0 = 13 (n)
# p - w = 15 - 22 = -7 = 19 (t)

# Clé: "cant" ?
print(f"Clé potentielle: cant")

# Essayons de décoder avec la clé "cant"
def vigenere_decode(ciphertext, key):
    result = ""
    key_idx = 0
    for c in ciphertext:
        if c.isalpha():
            base = ord('a') if c.islower() else ord('A')
            c_val = ord(c) - base
            k_val = ord(key[key_idx % len(key)].lower()) - ord('a')
            p_val = (c_val - k_val) % 26
            result += chr(p_val + base)
            key_idx += 1
        else:
            result += c
    return result

print(f"Décodé avec 'cant': {vigenere_decode(decoded, 'cant')}")

# Essayons d'autres clés possibles
for key in ['csaw', 'flag', 'find', 'keep', 'secret', 'hidden']:
    print(f"Décodé avec '{key}': {vigenere_decode(decoded, key)}")