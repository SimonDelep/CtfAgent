cipher = "esnp{d0c_@yz@gl_mn0j_pm3z3_g0_o00s}"
key = [6, 0, 15, 7, 0]

result = []
for i, c in enumerate(cipher):
    result.append(chr(ord(c) ^ key[i % len(key)]))
print("XOR avec clé [6,0,15,7,0]:", ''.join(result))

# Peut-être que la clé est différente. Essayons de deviner le flag en supposant
# que c'est un message lisible avec des mots anglais

# Si on suppose que le flag contient "the" ou "flag" ou d'autres mots communs
# on peut essayer de trouver la clé

# Autre idée : peut-être que c'est un décalage de chaque caractère par une valeur fixe
# ou un décalage basé sur la position

# Essayons un décalage simple (Caesar) sur toute la chaîne
for shift in range(26):
    result = []
    for c in cipher:
        if c.isalpha():
            if c.islower():
                result.append(chr((ord(c) - ord('a') + shift) % 26 + ord('a')))
            else:
                result.append(chr((ord(c) - ord('A') + shift) % 26 + ord('A')))
        else:
            result.append(c)
    print(f"Shift {shift}: {''.join(result)}")
