ciphertext = "esnp{d0c_@yz@gl_mn0j_pm3z3_g0_o00s}"
plaintext = "csaw{you_always_know_where_to_look}"

ct_letters = [c for c in ciphertext if c.isalpha()]
pt_letters = [c for c in plaintext if c.isalpha()]

print("Ciphertext lettres:", ''.join(ct_letters), "len:", len(ct_letters))
print("Plaintext lettres:", ''.join(pt_letters), "len:", len(pt_letters))

# Trouver la clé lettre par lettre
key_chars = []
for i in range(min(len(ct_letters), len(pt_letters))):
    c = ct_letters[i]
    p = pt_letters[i]
    base_c = ord('A') if c.isupper() else ord('a')
    base_p = ord('A') if p.isupper() else ord('a')
    shift = (ord(c) - base_c - (ord(p) - base_p)) % 26
    key_chars.append(chr(shift + ord('a')))

print("Clé lettre par lettre:", ''.join(key_chars))