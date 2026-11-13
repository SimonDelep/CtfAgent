encrypted = "esnp{d0c_@yz@gl_mn0j_pm3z3_g0_o00s}"

# Essayer tous les décalages Caesar possibles
for shift in range(26):
    decrypted = []
    for char in encrypted:
        if char.isalpha():
            base = ord('a') if char.islower() else ord('A')
            decrypted_char = chr((ord(char) - base + shift) % 26 + base)
            decrypted.append(decrypted_char)
        else:
            decrypted.append(char)
    result = ''.join(decrypted)
    if 'csaw' in result.lower():
        print(f"Shift {shift}: {result}")