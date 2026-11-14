# XOR de '2_5t3@1_' avec la clé \xaa\xc4\xc3D
target = b'2_5t3@1_'
key = bytes([0xaa, 0xc4, 0xc3, 0x44])

# XOR en répétant la clé
result = bytes([target[i] ^ key[i % len(key)] for i in range(len(target))])
print(f"XOR de '2_5t3@1_' avec la clé: {repr(result)}")
print(f"Hex: {result.hex()}")

# Essayer aussi l'inverse: clé XOR avec target
result2 = bytes([key[i % len(key)] ^ target[i] for i in range(len(target))])
print(f"Inverse: {repr(result2)}")

# Peut-être que le flag est simplement '2_5t3@1_' dans le format csaw{}
print(f"\nFlag possible: csaw{{2_5t3@1_}}")

# Vérifions si '2_5t3@1_' pourrait être une substitution de 'csaw{...}'
# '2' -> 'c', '_' -> 's', '5' -> 'a', 't' -> 'w', etc.
# 2_5t3@1_ = 8 caractères
# csaw{} = 6 caractères, donc pas une substitution directe

# Peut-être que le flag est 'csaw{2_5t3@1_}'
# Ou peut-être qu'il faut décoder les autres chaînes Base64