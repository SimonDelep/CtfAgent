# Les XOR sont: 6, 0, 15, 7
# Peut-être que c'est une clé qui se répète ou un pattern

# Regardons si ces valeurs correspondent à des caractères ASCII
xor_values = [6, 0, 15, 7]
print("Valeurs XOR en ASCII:")
for v in xor_values:
    if 32 <= v < 127:
        print(f"  {v} -> '{chr(v)}'")
    else:
        print(f"  {v} -> contrôle/non-imprimable")

# Peut-être que le préfixe est simplement "csaw" et que le reste est correct
# Essayons de soumettre directement avec csaw comme préfixe
content = "d0c_@yz@gl_mn0j_pm3z3_g0_o00s"
print(f"\nFlag possible: csaw{{{content}}}")

# Mais vérifions d'abord si le contenu entre accolades a un sens
# Peut-être que c'est un autre type de chiffrement

# Regardons les caractères spéciaux: @, _, 0, 3
# @ est ASCII 64, _ est 95
# Peut-être que c'est un décalage sur tous les caractères

print("\nAnalyse des caractères:")
for i, c in enumerate(content):
    print(f"  {i}: '{c}' = {ord(c)}")