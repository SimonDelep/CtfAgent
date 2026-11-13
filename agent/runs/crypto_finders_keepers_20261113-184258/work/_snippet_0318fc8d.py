# Vérifions le XOR
print(f"123 ^ 6 = {123 ^ 6} = {chr(123 ^ 6)}")
print(f"ord({chr(123)}) = {ord(chr(123))}")
print(f"ord({chr(125)}) = {ord(chr(125))}")

# Donc { ^ 6 = y, pas }
# Mais le résultat montre csaw}...

# Peut-être que la clé est différente pour le 5ème caractère
# Si { ^ k = {, alors k = 0
# Si { ^ k = }, alors k = 123 ^ 125 = 2

# Essayons avec une clé différente
decoded = "esnp{d0c_@yz@gl_mn0j_pm3z3_g0_o00s}"

# Si on veut que { reste {, la clé doit être 0
# Si on veut que { devienne }, la clé doit être 2

# Peut-être que la clé est [6, 0, 15, 7, 0, 0, 0, ...] (seulement les 4 premiers caractères sont XORés)
key = [6, 0, 15, 7]
result = ''
for i, c in enumerate(decoded):
    if i < 4:
        k = key[i]
    else:
        k = 0  # Pas de XOR pour le reste
    result += chr(ord(c) ^ k)

print(f"Résultat avec clé seulement sur les 4 premiers: {result}")