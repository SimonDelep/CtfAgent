# Comparaison pour trouver la clé XOR
observed = "esnp{d0c_@yz@gl_mn0j_pm3z3_g0_o00s}"
expected_prefix = "csaw{"

# Trouver la clé XOR pour les 5 premiers caractères
key_bytes = []
for i in range(5):
    key_bytes.append(ord(observed[i]) ^ ord(expected_prefix[i]))

print(f"Clé XOR déduite (5 premiers chars): {key_bytes}")
print(f"Clé en hex: {[hex(b) for b in key_bytes]}")

# Peut-être que la clé est plus longue ? Essayons de voir si c'est un motif répétitif
# ou si c'est une clé basée sur un mot