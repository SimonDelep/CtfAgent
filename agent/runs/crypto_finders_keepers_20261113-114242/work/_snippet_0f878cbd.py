# Vérifions le décodage caractère par caractère
cipher_full = "esnp{d0c_@yz@gl_mn0j_pm3z3_g0_o00s}"
key = "cant"

print("Décodage détaillé:")
result = []
key_index = 0
for i, char in enumerate(cipher_full):
    if char.isalpha():
        if char.isupper():
            base = ord('A')
        else:
            base = ord('a')
        cipher_val = ord(char) - base
        key_val = ord(key[key_index % len(key)].lower()) - ord('a')
        plain_val = (cipher_val - key_val) % 26
        plain_char = chr(plain_val + base)
        print(f"  {i}: '{char}' (key='{key[key_index % len(key)]}') -> '{plain_char}'")
        result.append(plain_char)
        key_index += 1
    else:
        result.append(char)
        print(f"  {i}: '{char}' -> '{char}' (non-alpha)")

print("\nRésultat final:", ''.join(result))