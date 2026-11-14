# Analyser les différences entre ciphertext et plaintext attendu
ciphertext = "esnp"
expected = "csaw"

for i, (c, e) in enumerate(zip(ciphertext, expected)):
    diff = (ord(c) - ord(e)) % 26
    print(f"Position {i}: '{c}' -> '{e}' : diff = {diff} (clé = '{chr(ord('a') + diff)}')")

# Vérifier si c'est un XOR simple
print("\nVérification XOR:")
for i, (c, e) in enumerate(zip(ciphertext, expected)):
    xor_val = ord(c) ^ ord(e)
    print(f"Position {i}: '{c}' ^ '{e}' = {xor_val} = '{chr(xor_val)}'")