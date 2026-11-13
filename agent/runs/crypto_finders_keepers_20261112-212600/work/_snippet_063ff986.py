# Redéfinissons la fonction
def xor_decrypt(ciphertext, key):
    result = []
    for i, c in enumerate(ciphertext):
        k = key[i % len(key)]
        result.append(chr(ord(c) ^ k))
    return ''.join(result)

key = [6, 0, 15, 7]
brut = "esnp{d0c_@yz@gl_mn0j_pm3z3_g0_o00s}"

result = xor_decrypt(brut, key)
print("Résultat complet:", result)

# Analysons les caractères
print("\nAnalyse des caractères:")
for i, c in enumerate(result):
    print(f"Position {i}: '{c}' (ord={ord(c)})")