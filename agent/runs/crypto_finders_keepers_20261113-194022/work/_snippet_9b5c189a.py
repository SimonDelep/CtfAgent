ciphertext = "esnp{d0c_@yz@gl_mn0j_pm3z3_g0_o00s}"
key = "cantfind"

# Analyser chaque caractère
print("Analyse caractère par caractère:")
print(f"{'Pos':<4} {'Char':<4} {'Ord':<4} {'KeyChar':<6} {'KeyOrd':<4} {'Decrypted':<6} {'DecOrd':<4}")
print("-" * 50)

result = []
key_idx = 0
for i, char in enumerate(ciphertext):
    if char.isalpha():
        base = ord('A') if char.isupper() else ord('a')
        key_char = key[key_idx % len(key)]
        key_shift = ord(key_char.lower()) - ord('a')
        decrypted = chr((ord(char) - base - key_shift) % 26 + base)
        result.append(decrypted)
        print(f"{i:<4} {char!r:<4} {ord(char):<4} {key_char:<6} {ord(key_char):<4} {decrypted!r:<6} {ord(decrypted):<4}")
        key_idx += 1
    else:
        result.append(char)
        print(f"{i:<4} {char!r:<4} {ord(char):<4} {'-':<6} {'-':<4} {char!r:<6} {ord(char):<4}")

print("\nRésultat:", ''.join(result))