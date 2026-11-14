ciphertext = "esnp{d0c_@yz@gl_mn0j_pm3z3_g0_o00s}"

# Décalage alterné: j=9, c=2
def decrypt_alternate(ciphertext, shifts):
    result = []
    shift_idx = 0
    for char in ciphertext:
        if char.isalpha():
            base = ord('A') if char.isupper() else ord('a')
            shift = shifts[shift_idx % len(shifts)]
            decrypted = chr((ord(char) - base - shift) % 26 + base)
            result.append(decrypted)
            shift_idx += 1
        else:
            result.append(char)
    return ''.join(result)

# j=9, c=2
print("Décalage alterné [9,2]:", decrypt_alternate(ciphertext, [9, 2]))
print("Décalage alterné [2,9]:", decrypt_alternate(ciphertext, [2, 9]))

# Peut-être que c'est l'inverse (chiffrement vs déchiffrement)
def encrypt_alternate(ciphertext, shifts):
    result = []
    shift_idx = 0
    for char in ciphertext:
        if char.isalpha():
            base = ord('A') if char.isupper() else ord('a')
            shift = shifts[shift_idx % len(shifts)]
            encrypted = chr((ord(char) - base + shift) % 26 + base)
            result.append(encrypted)
            shift_idx += 1
        else:
            result.append(char)
    return ''.join(result)

print("Chiffrement alterné [9,2]:", encrypt_alternate(ciphertext, [9, 2]))