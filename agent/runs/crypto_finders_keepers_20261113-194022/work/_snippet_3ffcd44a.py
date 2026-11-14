ciphertext = "esnp{d0c_@yz@gl_mn0j_pm3z3_g0_o00s}"
# Extraire seulement les lettres
letters_only = [c for c in ciphertext if c.isalpha()]
print("Toutes les lettres:", ''.join(letters_only))
print("Nombre de lettres:", len(letters_only))

# Après le préfixe csaw{
content = ciphertext[5:-1]  # Enlever csaw{ et }
print("\nContenu entre accolades:", content)
letters_content = [c for c in content if c.isalpha()]
print("Lettres dans le contenu:", ''.join(letters_content))
print("Nombre de lettres dans le contenu:", len(letters_content))

# Avec la clé cantfind, combien de lettres sont chiffrées?
key = "cantfind"
print(f"\nLongueur de la clé: {len(key)}")
print(f"Si on répète la clé: {key * (len(letters_content) // len(key) + 1)}")