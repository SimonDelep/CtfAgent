# Let's think about this differently
# The ciphertext is: esnp{d0c_@yz@gl_mn0j_pm3z3_g0_o00s}
# Decrypted with "cantfindit": csaw{y0u_@lw@ys_kn0w_wh3r3_t0_l00k}

# What if "jc" means we need to look at the video frames themselves?
# Or maybe there's steganography in the video?

# Let's also consider that "jc" might be a hint about the format
# Maybe the flag should be in a specific format?

# Another thought: what if "jc" is actually part of the key?
# Like "cantfinditjc" or "jc" appended/prepended?

ciphertext = "esnp{d0c_@yz@gl_mn0j_pm3z3_g0_o00s}"

def vigenere_decrypt(ct, k):
    result = []
    k_idx = 0
    for c in ct:
        if c.isalpha():
            base = ord('A') if c.isupper() else ord('a')
            shift = ord(k[k_idx % len(k)].lower()) - ord('a')
            result.append(chr((ord(c) - base - shift) % 26 + base))
            k_idx += 1
        else:
            result.append(c)
    return ''.join(result)

# Try "cantfinditjc" as key
print("With 'cantfinditjc':", vigenere_decrypt(ciphertext, "cantfinditjc"))

# Try "jc" as the key (we already know this gives gibberish)
print("With 'jc':", vigenere_decrypt(ciphertext, "jc"))

# What if "jc" means we should use a different cipher entirely?
# Like Atbash? Or a combination?

def atbash(text):
    result = []
    for c in text:
        if c.isalpha():
            base = ord('A') if c.isupper() else ord('a')
            result.append(chr(base + 25 - (ord(c) - base)))
        else:
            result.append(c)
    return ''.join(result)

print("Atbash of ciphertext:", atbash(ciphertext))
print("Atbash of plaintext:", atbash("csaw{y0u_@lw@ys_kn0w_wh3r3_t0_l00k}"))

# What if the plaintext needs to be transformed?
plaintext = "csaw{y0u_@lw@ys_kn0w_wh3r3_t0_l00k}"
content = plaintext[5:-1]
print(f"Content: {content}")

# Maybe the flag is just "you_always_know_where_to_look" but we need to submit it differently?
# Or maybe there's a different message hidden?