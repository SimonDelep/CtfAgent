# Essayons de deviner le texte clair et retrouver la clé
ciphertext = "esnp{d0c_@yz@gl_mn0j_pm3z3_g0_o00s}"

# Si le texte clair attendu est "you_always_be_here_to_off" ou similaire
# Regardons la partie après csaw{
# ciphertext après { : d0c_@yz@gl_mn0j_pm3z3_g0_o00s

# Essayons de deviner ce que pourrait être le message
# "you_always" serait une bonne hypothèse
# Comparons:
# ciphertext: d 0 c _ @ y z @ g l m n 0 j p m 3 z 3 _ g 0 _ o 0 0 s
# clair attendu: y o u _ a l w a y s _ b e _ h e r e _ t o _ o f f

# Pour les lettres seulement (en ignorant chiffres et symboles):
# ciphertext lettres: d c y z g l m n j p m z z g o s
# clair attendu lettres: y o u a l w a y s b e h e r e t o f f

# Calculons les décalages nécessaires
ciph_letters = [c for c in "d0c_@yz@gl_mn0j_pm3z3_g0_o00s" if c.isalpha()]
plain_guess = list("youalwaystobehereoff")  # Hypothèse

print("Ciphertext lettres:", ''.join(ciph_letters))
print("Clair supposé:", ''.join(plain_guess))

if len(ciph_letters) == len(plain_guess):
    key_needed = []
    for i, (c, p) in enumerate(zip(ciph_letters, plain_guess)):
        base = ord('a')
        shift = (ord(p) - ord(c)) % 26
        key_char = chr(base + shift)
        key_needed.append(key_char)
        print(f"{c} -> {p} : shift {shift} -> '{key_char}'")
    print("\nClé déduite:", ''.join(key_needed))