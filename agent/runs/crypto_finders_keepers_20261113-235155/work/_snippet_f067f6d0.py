# Let's think about "jc" differently
# Maybe "jc" is a key for a different cipher?
# Or maybe we need to apply jc transformation?

ciphertext = "esnp{d0c_@yz@gl_mn0j_pm3z3_g0_o00s}"
key_cantfindit = "cantfindit"

# What if "jc" means we should use a different approach?
# Let's try interpreting "jc" as indices or something

# j = 9, c = 2 (0-indexed: j=9, c=2)
# Or maybe it's about the position in alphabet: j=10, c=3 (1-indexed)

# What if we need to apply a ROT or Caesar with "jc"?
# j -> 9, c -> 2

def caesar(text, shift):
    result = []
    for c in text:
        if c.isalpha():
            base = ord('A') if c.isupper() else ord('a')
            result.append(chr((ord(c) - base + shift) % 26 + base))
        else:
            result.append(c)
    return ''.join(result)

# Try various interpretations of "jc"
print("Testing 'jc' as potential cipher parameters:")
print(f"j=9, c=2: caesar with shift 9: {caesar(ciphertext, 9)}")
print(f"j=9, c=2: caesar with shift 2: {caesar(ciphertext, 2)}")

# What if "jc" means we should swap letters at positions j and c?
# Or use it as a key for a different cipher?

# Let's also check if the plaintext itself has something special
plaintext = "csaw{y0u_@lw@ys_kn0w_wh3r3_t0_l00k}"
print(f"\nPlaintext: {plaintext}")

# Maybe the flag is simply the content without csaw{}?
content = plaintext[5:-1]
print(f"Content only: {content}")

# Or maybe we need to convert leet to normal?
leet_to_normal = content.replace('0', 'o').replace('@', 'a').replace('3', 'e')
print(f"Cleaned: {leet_to_normal}")