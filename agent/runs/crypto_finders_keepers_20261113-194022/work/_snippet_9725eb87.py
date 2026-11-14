# Texte déchiffré avec clé 'cantfindit'
decrypted = "csaw{y0u_@lw@ys_kn0w_wh3r3_t0_l00k}"
print(f"Texte déchiffré brut: {decrypted}")

# Substitution Leet Speak
leet_map = {'0': 'o', '@': 'a', '3': 'e', '1': 'i', '5': 's', '7': 't'}
cleaned = decrypted
for leet, plain in leet_map.items():
    cleaned = cleaned.replace(leet, plain)
print(f"Après substitution Leet: {cleaned}")

# Vérifions aussi si le texte brut pourrait être le flag
print(f"Flag candidat brut: {decrypted}")
print(f"Flag candidat nettoyé: {cleaned}")