# Le flag brut décodé
brut = "esnp{d0c_@yz@gl_mn0j_pm3z3_g0_o00s}"

# Différences pour transformer esnp en csaw
# e(101) -> c(99) : -2
# s(115) -> s(115) : 0
# n(110) -> a(97) : -13
# p(112) -> w(119) : +7

# En XOR :
# e XOR c = 6
# s XOR s = 0
# n XOR a = 23
# p XOR w = 7

key_xor = [6, 0, 23, 7]

# Appliquons XOR avec cette clé sur tout le contenu
def xor_decrypt(ciphertext, key):
    result = []
    for i, c in enumerate(ciphertext):
        k = key[i % len(key)]
        result.append(chr(ord(c) ^ k))
    return ''.join(result)

# Test sur le préfixe
print("Préfixe XOR:", xor_decrypt("esnp", key_xor))

# Test sur tout le contenu
print("Déchiffrement complet:", xor_decrypt(brut, key_xor))

# Essayons aussi avec une clé basée sur les différences de décalage
# Peut-être que c'est un décalage positionnel ?
print("\n--- Tentative avec décalage positionnel ---")
# Si la clé est la position mod quelque chose...
for shift in range(26):
    decoded = ''.join(chr((ord(c) - 97 - shift) % 26 + 97) if c.isalpha() else c for c in brut)
    if decoded.startswith("csaw"):
        print(f"ROT{shift}:", decoded)