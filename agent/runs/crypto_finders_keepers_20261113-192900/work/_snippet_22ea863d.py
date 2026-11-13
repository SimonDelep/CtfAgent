from vigenere_decrypt import vigenere_decrypt

ciphertext = "esnp{d0c_@yz@gl_mn0j_pm3z3_g0_o00s}"

# Essayons différentes clés
keys_to_try = ["jc", "canva", "finders", "keepers", "cant", "cantfind", "find", "keep", "engine"]

for key in keys_to_try:
    try:
        result = vigenere_decrypt(ciphertext, key)
        print(f"Clé '{key}': {result}")
    except Exception as e:
        print(f"Clé '{key}': Erreur - {e}")