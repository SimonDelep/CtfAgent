# Texte chiffré trouvé dans les métadonnées
encrypted = "esnp{d0c_@yz@gl_mn0j_pm3z3_g0_o00s}"
# Préfixe attendu
expected_prefix = "csaw{"

# Calculons la clé XOR pour le préfixe
key_prefix = [ord(e) ^ ord(p) for e, p in zip(encrypted[:5], expected_prefix)]
print(f"Clé XOR du préfixe: {key_prefix}")

# Maintenant, essayons de trouver un motif dans la clé
# Si on suppose que le flag complet est de la forme csaw{...}, calculons la clé complète
# en supposant que le reste du flag est lisible

# Calculons la clé XOR caractère par caractère
# On va supposer que le texte attendu est aussi lisible (lettres, chiffres, underscores)
# et chercher un motif dans la séquence XOR

print("\nAnalyse caractère par caractère:")
for i, (enc, exp) in enumerate(zip(encrypted, expected_prefix)):
    xor_val = ord(enc) ^ ord(exp)
    print(f"Pos {i}: '{enc}' XOR '{exp}' = {xor_val} (0x{xor_val:02x})")

# Maintenant, cherchons si la clé est basée sur la position
print("\nVérifions si XOR avec la position donne un motif:")
for i, c in enumerate(encrypted):
    xor_pos = ord(c) ^ i
    print(f"Pos {i}: '{c}' XOR {i} = {xor_pos} -> '{chr(xor_pos) if 32 <= xor_pos < 127 else '?'}'")