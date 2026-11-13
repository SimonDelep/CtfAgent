payload = "d0c_@yz@gl_mn0j_pm3z3_g0_o00s"

# Substitutions courantes
substitutions = {
    '0': 'o',
    '3': 'e',
    '@': 'a',  # tentative 1
    '_': ' ',
}

decoded = ""
for c in payload:
    decoded += substitutions.get(c, c)

print("Avec @='a':", decoded)

# Essayons @='t'
substitutions2 = {
    '0': 'o',
    '3': 'e',
    '@': 't',  # tentative 2
    '_': ' ',
}

decoded2 = ""
for c in payload:
    decoded2 += substitutions2.get(c, c)

print("Avec @='t':", decoded2)

# Essayons @='s'
substitutions3 = {
    '0': 'o',
    '3': 'e',
    '@': 's',  # tentative 3
    '_': ' ',
}

decoded3 = ""
for c in payload:
    decoded3 += substitutions3.get(c, c)

print("Avec @='s':", decoded3)