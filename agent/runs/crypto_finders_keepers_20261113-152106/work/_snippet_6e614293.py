text = "csaw{y0u_@lw@el_zu0e_hz3w3_e0_o00f}"

# Substitutions Leet Speak
leet_map = {
    '0': 'o',
    '@': 'a',
    '3': 'e',
    '1': 'i',
    '5': 's',
    '7': 't',
    '4': 'a',
    '2': 'z',
    '8': 'b',
    '9': 'g',
    '6': 'g',
    'l': 'l',  # garde 'l' tel quel
}

result = []
for c in text:
    if c in leet_map:
        result.append(leet_map[c])
    else:
        result.append(c)

decoded = ''.join(result)
print(f"Après substitution Leet: {decoded}")

# Vérifions les mots
import re
words = re.findall(r'[a-z_]+', decoded)
print(f"Mots: {words}")