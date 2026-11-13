# Texte chiffré
encrypted = "esnp{d0c_@yz@gl_mn0j_pm3z3_g0_o00s}"

# Clé XOR déduite du préfixe
key = [6, 0, 15, 7, 0]

# Essayons de décoder avec cette clé cyclique
def xor_decrypt(text, key):
    result = []
    for i, c in enumerate(text):
        k = key[i % len(key)]
        result.append(chr(ord(c) ^ k))
    return ''.join(result)

decrypted = xor_decrypt(encrypted, key)
print(f"Décrypté avec clé {key}: {decrypted}")

# La clé semble être [6, 0, 15, 7, 0] mais le résultat n'est pas lisible
# Essayons de trouver une clé qui donne un flag lisible

# On sait que le flag commence par "csaw{"
# Calculons la clé nécessaire pour chaque position
print("\nClé nécessaire pour obtenir 'csaw{...}':")
expected = "csaw{"
for i, (enc, exp) in enumerate(zip(encrypted, expected)):
    print(f"Pos {i}: '{enc}' -> '{exp}' nécessite XOR {ord(enc) ^ ord(exp)}")

# Maintenant, regardons si on peut deviner le reste du flag
# Le format est csaw{...} avec des caractères alphanumériques et underscores
# Essayons de trouver un motif dans les valeurs XOR

# Peut-être que la clé est basée sur le nom du challenge "finderskeepers"
challenge_name = "finderskeepers"
print(f"\nEssai avec clé = 'finderskeepers':")
key_from_name = [ord(c) for c in challenge_name]
decrypted_name = xor_decrypt(encrypted, key_from_name)
print(f"Décrypté: {decrypted_name}")

# Ou peut-être que la clé est simplement la position XOR quelque chose
# Regardons les valeurs XOR nécessaires si on suppose que le flag est lisible
print("\nAnalyse des valeurs XOR si on suppose un flag lisible:")
# On va essayer de trouver un motif en regardant les différences