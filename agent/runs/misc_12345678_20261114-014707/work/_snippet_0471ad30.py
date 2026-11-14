# Analysons la relation entre '2_5t3@1_' et 'csaw{...}'
# Peut-être que chaque caractère est XORé avec quelque chose

target = "2_5t3@1_"
# Le format flag est csaw{...} donc peut-être que 2_5t3@1_ est le contenu entre les accolades
# Ou peut-être que c'est une substitution

# Essayons de voir si c'est un décalage simple (ROT)
for shift in range(26):
    result = ""
    for c in target:
        if c.isalpha():
            base = ord('a') if c.islower() else ord('A')
            result += chr((ord(c) - base + shift) % 26 + base)
        else:
            result += c
    print(f"ROT{shift}: {result}")

print("\n---")
# Essayons XOR avec des clés simples
for key in range(256):
    result = ""
    for c in target:
        result += chr(ord(c) ^ key)
    if result.startswith('c') and 'saw' in result:
        print(f"XOR avec {key}: {repr(result)}")