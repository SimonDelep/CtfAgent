# Re-examinons le ciphertext et le plaintext partiel
ciphertext = "esnp{d0c_@yz@gl_mn0j_pm3z3_g0_o00s}"
key = "cant"

# Le plaintext après Vigenère est: csaw{b0c_@lg@el_zu0h_pz3g3_e0_o00f}
# Essayons de deviner le flag correct en analysant la structure

# Format attendu: csaw{...}
# Le plaintext partiel: csaw{b0c_@lg@el_zu0h_pz3g3_e0_o00f}

# Hypothèses:
# - "b0c" pourrait être "doc" (0=o) -> "doc"
# - "@lg@el" pourrait être "_algo_" ou "_alg_el" -> @ = _ ?
# - "zu0h" pourrait être "zoom" (0=o, h=m?) ou "zoo" 
# - "pz3g3" pourrait être "page" (3=e) -> "pege" ou "page"
# - "e0" pourrait être "eo" ou "to"
# - "o00f" pourrait être "ooof" ou "oof"

# Essayons une approche différente: peut-être que le ciphertext original a des caractères
# qui ne sont pas des lettres et qui doivent être traités différemment

# Regardons le ciphertext caractère par caractère
print("Analyse caractère par caractère:")
for i, c in enumerate(ciphertext):
    print(f"{i}: '{c}' (ord={ord(c)})")