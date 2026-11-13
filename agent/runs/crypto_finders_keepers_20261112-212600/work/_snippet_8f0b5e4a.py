# Décodage du leet speak
payload = "d0c_@yz@gl_mn0j_pm3z3_g0_o00s"

# Substitutions courantes en leet speak
leet_map = {
    '0': 'o',
    '1': 'i',
    '3': 'e',
    '4': 'a',
    '5': 's',
    '7': 't',
    '@': 'a',  # tentative
    '_': ' ',
}

# Appliquer les substitutions
decoded = ""
for c in payload:
    decoded += leet_map.get(c, c)

print("Décodage simple:", decoded)

# Essayons avec @ = 't'
leet_map2 = {
    '0': 'o',
    '1': 'i',
    '3': 'e',
    '4': 'a',
    '5': 's',
    '7': 't',
    '@': 't',  # autre tentative
    '_': ' ',
}

decoded2 = ""
for c in payload:
    decoded2 += leet_map2.get(c, c)

print("Avec @='t':", decoded2)

# Essayons @ = 'a'
decoded3 = ""
for c in payload:
    decoded3 += leet_map.get(c, c)

print("Avec @='a':", decoded3)