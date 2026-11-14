# Let's verify the Vigenère decryption and explore the "jc" hint
ciphertext = "esnp{d0c_@yz@gl_mn0j_pm3z3_g0_o00s}"
key = "cantfindit"

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

decrypted = vigenere_decrypt(ciphertext, key)
print(f"Ciphertext: {ciphertext}")
print(f"Decrypted:  {decrypted}")
print(f"Length: {len(decrypted)}")

# The "jc" hint - maybe it's a JSON format?
# Or maybe we need to use the actual "jc" tool?
# Let's also check if there's something in the video frames themselves
print("\n--- Exploring 'jc' hint ---")
print("jc is a JSON CLI tool - maybe the flag should be JSON formatted?")
print(f"Possible JSON: {{\"flag\": \"{decrypted}\"}}")
print(f"Or just the content: {decrypted[5:-1]}")  # Remove csaw{}