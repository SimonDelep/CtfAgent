decoded = "esnp{d0c_@yz@gl_mn0j_pm3z3_g0_o00s}"
key = [6, 0, 15, 7]

result = ''
for i, c in enumerate(decoded):
    k = key[i % len(key)]
    result += chr(ord(c) ^ k)

print(f"Résultat XOR avec clé [6,0,15,7]: {result}")

# Peut-être que la clé est différente. Essayons de trouver la clé qui transforme 'esnp' en 'csaw'
# e (101) ^ k0 = c (99) => k0 = 6
# s (115) ^ k1 = s (115) => k1 = 0
# n (110) ^ k2 = a (97) => k2 = 15
# p (112) ^ k3 = w (119) => k3 = 7

# Donc la clé est [6, 0, 15, 7]
# Mais si on applique cette clé à tout le message, on obtient un résultat bizarre.

# Peut-être que le message est déjà correct et qu'il faut juste soumettre 'esnp{d0c_@yz@gl_mn0j_pm3z3_g0_o00s}'
# Mais le format du flag est csaw{...}, donc peut-être que le message décodé est 'esnp{d0c_@yz@gl_mn0j_pm3z3_g0_o00s}'
# et le flag est csaw{esnp_d0c_yz_gl_mn0j_pm3z3_g0_o00s} (en enlevant les caractères spéciaux)

# Ou peut-être que le message décodé est 'csaw{d0c_@yz@gl_mn0j_pm3z3_g0_o00s}' et qu'il faut le soumettre sans le wrapper
# Donc le flag serait csaw{d0c_@yz@gl_mn0j_pm3z3_g0_o00s}

# En fait, la description dit "Submit the decoded plaintext without a flag wrapper."
# Donc si le message décodé est 'csaw{d0c_@yz@gl_mn0j_pm3z3_g0_o00s}', le flag serait csaw{csaw{d0c_@yz@gl_mn0j_pm3z3_g0_o00s}} ? Non, ça n'a pas de sens.

# Peut-être que le message décodé est 'esnp{d0c_@yz@gl_mn0j_pm3z3_g0_o00s}' et qu'il faut le soumettre tel quel,
# mais en remplaçant 'esnp' par 'csaw' ?

# Essayons de soumettre 'csaw{d0c_@yz@gl_mn0j_pm3z3_g0_o00s}'
print("Candidat flag: csaw{d0c_@yz@gl_mn0j_pm3z3_g0_o00s}")