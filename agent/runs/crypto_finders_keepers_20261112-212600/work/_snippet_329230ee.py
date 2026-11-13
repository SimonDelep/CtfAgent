ciphertext = "esnp{d0c_@yz@gl_mn0j_pm3z3_g0_o00s}"

# Clé connue pour le préfixe
key_prefix = [6, 0, 15, 7]

# Décryptage avec la clé cyclique
def xor_decrypt(ct, key):
    result = []
    for i, c in enumerate(ct):
        k = key[i % len(key)]
        result.append(chr(ord(c) ^ k))
    return ''.join(result)

# Test avec la clé [6, 0, 15, 7]
print("Avec clé [6, 0, 15, 7]:")
print(xor_decrypt(ciphertext, key_prefix))

# Test: quelle clé donnerait csaw{...} ?
# e^k0=c, s^k1=s, n^k2=a, p^k3=w
# {^k4={, d^k5=d, 0^k6=0, c^k7=c, _^k8=_, @^k9=_, y^k10=z, z^k11=...
print("\nAnalyse des clés nécessaires:")
plaintext_wanted = "csaw{d0c_"  # ce qu'on veut obtenir
for i, (ct_char, pt_char) in enumerate(zip(ciphertext, plaintext_wanted)):
    needed_key = ord(ct_char) ^ ord(pt_char)
    print(f"pos {i}: '{ct_char}' ^ {needed_key} = '{pt_char}'")