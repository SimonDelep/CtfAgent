# Analyser la transformation caractère par caractère
chiffre = "esnp{d0c_@yz@gl_mn0j_pm3z3_g0_o00s}"
attendu_prefixe = "csaw{"

# La clé XOR pour les 5 premiers chars est [6, 0, 15, 7, 0]
# Peut-être que la clé est basée sur la position ou un motif

# Vérifions si c'est un XOR avec une clé qui change selon une règle
# Par exemple, XOR avec la position, ou XOR avec une clé dérivée

# Essayons de voir si la clé est simplement [6, 0, 15, 7, 0] répété
cle_base = [6, 0, 15, 7, 0]
resultat = ""
for i, c in enumerate(chiffre):
    k = cle_base[i % len(cle_base)]
    resultat += chr(ord(c) ^ k)
print("XOR avec clé [6,0,15,7,0] répétée:")
print(resultat)
print("Représentation hex:")
print(' '.join(f'{ord(c):02x}' for c in resultat))

# Peut-être que la clé est dérivée du nom du fichier ou d'autre chose
# Essayons avec "finderskeepers" mais en XOR positionnel
print("\n---")
# Autre idée: peut-être que seul le préfixe est XORé, et le reste est autre chose
# Ou peut-être que c'est un chiffrement de Vigenère

# Vérifions les différences entre les caractères chiffrés et attendus
print("Différences (ord(c) - ord(a)):")
for i, (c, a) in enumerate(zip(chiffre[:20], "csaw{d0c_@yz@gl_mn0j")):
    print(f"  pos {i}: '{c}'({ord(c)}) -> '{a}'({ord(a)}), diff={ord(c)-ord(a)}, xor={ord(c)^ord(a)}")
