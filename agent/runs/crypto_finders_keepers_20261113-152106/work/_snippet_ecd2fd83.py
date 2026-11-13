# Trouver la clé Vigenère qui transforme 'esnp' en 'csaw'
ciphertext = "esnp"
plaintext = "csaw"

key = []
for c, p in zip(ciphertext, plaintext):
    # Vigenère: ciphertext = (plaintext + key) % 26
    # Donc: key = (ciphertext - plaintext) % 26
    diff = (ord(c) - ord(p)) % 26
    key.append(chr(ord('a') + diff))
    
print(f"Clé déduite: {''.join(key)}")

# Vérifions avec le reste du texte
# Le texte complet est: esnp{d0c_@yz@gl_mn0j_pm3z3_g0_o00s}
# On veut obtenir: csaw{...}

# Essayons de décoder avec la clé trouvée
ciphertext_full = "esnp{d0c_@yz@gl_mn0j_pm3z3_g0_o00s}"
key_str = ''.join(key)
print(f"Clé: {key_str}")

# Appliquer Vigenère inverse
def vigenere_decrypt(ciphertext, key):
    result = []
    key_idx = 0
    for c in ciphertext:
        if c.isalpha():
            base = ord('a') if c.islower() else ord('A')
            shift = ord(key[key_idx % len(key)]) - ord('a')
            decrypted = chr((ord(c) - base - shift) % 26 + base)
            result.append(decrypted)
            key_idx += 1
        else:
            result.append(c)
    return ''.join(result)

decrypted = vigenere_decrypt(ciphertext_full, key_str)
print(f"Décrypté avec clé '{key_str}': {decrypted}")