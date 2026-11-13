# Trouver la clé XOR
encrypted = "esnp{d0c_@yz@gl_mn0j_pm3z3_g0_o00s}"
expected_prefix = "csaw"

# Calculer la clé XOR pour les 4 premiers caractères
key = []
for i in range(4):
    xor_val = ord(encrypted[i]) ^ ord(expected_prefix[i])
    key.append(xor_val)
    print(f"'{encrypted[i]}' ^ {xor_val} = '{expected_prefix[i]}'")

print(f"Clé XOR: {key}")

# Essayer d'appliquer cette clé à tout le message
# Si la clé est répétitive, on peut essayer de la répéter
key_str = bytes(key)
print(f"Clé en bytes: {key_str}")

# Peut-être que la clé est une séquence de bytes
# Essayons de voir si c'est une clé simple comme 0x06, 0x00, 0x0F, 0x07