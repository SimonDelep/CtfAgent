ciphertext = "esnp{d0c_@yz@gl_mn0j_pm3z3_g0_o00s}"

# 'j' = 9, 'c' = 2 (0-indexed: a=0, b=1, c=2, ..., j=9)
# Peut-être que la clé est [9, 2] appliquée alternativement

def vigenere_decrypt_with_shifts(ciphertext, shifts):
    result = []
    shift_idx = 0
    for c in ciphertext:
        if c.isalpha():
            shift = shifts[shift_idx % len(shifts)]
            if c.islower():
                result.append(chr((ord(c) - ord('a') - shift) % 26 + ord('a')))
            else:
                result.append(chr((ord(c) - ord('A') - shift) % 26 + ord('A')))
            shift_idx += 1
        else:
            result.append(c)
    return ''.join(result)

# Essayer avec [9, 2]
print("Shifts [9, 2]:", vigenere_decrypt_with_shifts(ciphertext, [9, 2]))

# Essayer avec [2, 9]
print("Shifts [2, 9]:", vigenere_decrypt_with_shifts(ciphertext, [2, 9]))

# Peut-être que 'jc' signifie quelque chose d'autre
# 'j' est la 10ème lettre, 'c' est la 3ème lettre (1-indexed)
# Donc [10, 3] ou [9, 2] en 0-indexed

# Essayons d'autres interprétations de 'jc'
# Peut-être que c'est 'jc' comme clé Vigenère, mais appliquée seulement aux lettres du ciphertext
# Ce que nous faisons déjà avec la clé 'cantfindit'

# Attends, peut-être que le vrai message est différent
# Le ciphertext est 'esnp{...}' et avec 'cantfindit' on obtient 'csaw{...}'
# Mais peut-être que le message final n'est pas 'you_always_know_where_to_look'

# Essayons de voir si le message déchiffré avec 'cantfindit' a un sens différent
# 'y0u_@lw@ys_kn0w_wh3r3_t0_l00k' en Leet speak
# 'y0u' = 'you', '@lw@ys' = 'always', 'kn0w' = 'know', 'wh3r3' = 'where', 't0' = 'to', 'l00k' = 'look'
# Donc 'you_always_know_where_to_look'

# Mais peut-être que le flag est différent?
# L'indice dit "without a flag wrapper" - peut-être que le wrapper est autre chose?

# Ou peut-être que le message est en fait 'csaw{you_always_know_where_to_look}' et qu'on doit soumettre avec le wrapper?

# Essayons de soumettre différentes variantes
print("\nVariantes possibles:")
print("1. csaw{y0u_@lw@ys_kn0w_wh3r3_t0_l00k}")
print("2. csaw{you_always_know_where_to_look}")
print("3. y0u_@lw@ys_kn0w_wh3r3_t0_l00k")
print("4. you_always_know_where_to_look")

# Peut-être que le message est différent et qu'on a mal déchiffré
# Re-vérifions le déchiffrement avec 'cantfindit'

def vigenere_decrypt(ciphertext, key):
    result = []
    key_idx = 0
    for c in ciphertext:
        if c.isalpha():
            shift = ord(key[key_idx % len(key)].lower()) - ord('a')
            if c.islower():
                result.append(chr((ord(c) - ord('a') - shift) % 26 + ord('a')))
            else:
                result.append(chr((ord(c) - ord('A') - shift) % 26 + ord('A')))
            key_idx += 1
        else:
            result.append(c)
    return ''.join(result)

ciphertext = "esnp{d0c_@yz@gl_mn0j_pm3z3_g0_o00s}"
key = "cantfindit"
result = vigenere_decrypt(ciphertext, key)
print(f"\nDéchiffrement avec '{key}': {result}")

# Vérifions caractère par caractère
print("\nVérification caractère par caractère:")
for i, (c, k) in enumerate(zip(ciphertext, key * (len(ciphertext) // len(key) + 1))[:len(ciphertext)]):
    if c.isalpha():
        shift = ord(k.lower()) - ord('a')
        decrypted = chr((ord(c) - ord('a') - shift) % 26 + ord('a')) if c.islower() else chr((ord(c) - ord('A') - shift) % 26 + ord('A'))
        print(f"  {c} - {k} (shift {shift}) -> {decrypted}")
    else:
        print(f"  {c} (non-alphabétique) -> {c}")
