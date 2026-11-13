# @ est ASCII 64
# Si @ = espace (32), alors 64 XOR x = 32 => x = 64 XOR 32 = 96
print("@ (64) XOR 96 =", chr(64 ^ 96))  # devrait donner espace

# Vérifions le contenu avec @ = espace
content = "d0c_@yz@gl_mn0j_pm3z3_g0_o00s"
content_space = content.replace("@", " ")
print("Contenu avec @ = espace:", content_space)

# Peut-être que le flag est csaw{d0c yz gl mn0j pm3z3 g0 o00s}
# Mais les flags CTF ont généralement des underscores