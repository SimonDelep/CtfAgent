# Vérifions le texte Base64 décodé et essayons de trouver le flag correct
# Le texte déchiffré avec clé 'cantfind' est: csaw{y0u_@lw@el_zu0e_hz3w3_e0_o00f}

# Essayons de deviner le flag correct en corrigeant les mots
# y0u -> you
# @lw@el -> always (mais c'est alwael, donc peut-être que le texte original est alwael)
# zu0e -> true ? ou zoo ?
# hz3w3 -> here ?
# e0 -> to ?
# o00f -> off ?

# Le flag pourrait être: csaw{you_always_true_here_to_off}
# Ou: csaw{you_always_here_to_off}

# Mais le texte déchiffré est: csaw{y0u_@lw@el_zu0e_hz3w3_e0_o00f}
# Après substitution Leet: csaw{you_alwael_zuoe_hzewe_eo_ooof}

# Peut-être que le flag est exactement ce texte après substitution Leet
# csaw{you_alwael_zuoe_hzewe_eo_ooof}

# Ou peut-être que le flag est le texte déchiffré sans substitution Leet
# csaw{y0u_@lw@el_zu0e_hz3w3_e0_o00f}

# Essayons de soumettre le flag après substitution Leet
flag_candidate = "csaw{you_alwael_zuoe_hzewe_eo_ooof}"
print(f"Candidat 1: {flag_candidate}")

# Ou le flag original déchiffré
flag_candidate2 = "csaw{y0u_@lw@el_zu0e_hz3w3_e0_o00f}"
print(f"Candidat 2: {flag_candidate2}")

# Ou peut-être que le flag est: csaw{you_always_here_to_off}
flag_candidate3 = "csaw{you_always_here_to_off}"
print(f"Candidat 3: {flag_candidate3}")