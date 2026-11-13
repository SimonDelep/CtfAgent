# La clé XOR correcte est [6, 0, 15, 7]
key_xor = [6, 0, 15, 7]

brut = "esnp{d0c_@yz@gl_mn0j_pm3z3_g0_o00s}"

def xor_decrypt(ciphertext, key):
    result = []
    for i, c in enumerate(ciphertext):
        k = key[i % len(key)]
        result.append(chr(ord(c) ^ k))
    return ''.join(result)

# Test sur le préfixe
print("Préfixe XOR:", xor_decrypt("esnp", key_xor))

# Test sur tout le contenu
result = xor_decrypt(brut, key_xor)
print("Déchiffrement complet:", result)

# Vérifions si ça ressemble à un flag valide
if result.startswith("csaw{"):
    print("\nFlag potentiel:", result)