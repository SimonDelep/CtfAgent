# Les XOR sont: 6, 0, 15, 7
# Essayons de voir si c'est un décalage Vigenère avec une clé
# e -> c : décalage -2 (ou +24)
# s -> s : décalage 0
# n -> a : décalage -13 (ou +13)
# p -> w : décalage +7

# Vérifions les décalages en sens inverse (comment passer de csaw à esnp)
# c -> e : +2
# s -> s : 0
# a -> n : +13
# w -> p : -7 (ou +19)

print("Décalages pour transformer csaw en esnp:")
print(f"  c->e: {ord('e') - ord('c')}")
print(f"  s->s: {ord('s') - ord('s')}")
print(f"  a->n: {ord('n') - ord('a')}")
print(f"  w->p: {ord('p') - ord('w')}")

# Peut-être que la clé est basée sur les positions ou quelque chose comme ça
# Ou peut-être que c'est un chiffrement affine

# Essayons de décoder tout le message avec une clé Vigenère
def vigenere_decrypt(ciphertext, key):
    result = ""
    key_idx = 0
    for c in ciphertext:
        if c.isalpha():
            base = ord('A') if c.isupper() else ord('a')
            key_char = key[key_idx % len(key)]
            key_val = ord(key_char.lower()) - ord('a')
            decoded = chr((ord(c) - base - key_val) % 26 + base)
            result += decoded
            key_idx += 1
        else:
            result += c
    return result

# Essayons quelques clés courtes
encrypted = "esnp{d0c_@yz@gl_mn0j_pm3z3_g0_o00s}"
ciphertext = encrypted[4:]  # {d0c_@yz@gl_mn0j_pm3z3_g0_o00s}
print("\nTest Vigenère sur le contenu:")
for key in ["CSAW", "KEY", "FLAG", "SECRET", "FIND", "KEEP", "VIDEO", "HIDDEN"]:
    print(f"Clé '{key}': {vigenere_decrypt(ciphertext, key)}")