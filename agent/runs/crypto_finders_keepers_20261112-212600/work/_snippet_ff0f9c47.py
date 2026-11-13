content = "d0c_@yz@gl_mn0j_pm3z3_g0_o00s"

# Essayons de voir si c'est du Base64 avec des caractères modifiés
# Les caractères @ et _ pourraient être des substitutions

# Remplaçons @ par + et _ par / (caractères courants en Base64)
import base64

# Option 1: @ -> +, _ -> /
modified = content.replace('@', '+').replace('_', '/')
print(f"Avec @->+ et _->/: {modified}")
try:
    decoded = base64.b64decode(modified + '==')  # padding
    print(f"Décodé: {decoded}")
except Exception as e:
    print(f"Erreur: {e}")

# Option 2: Peut-être que c'est du Base64 URL-safe où _ et - sont utilisés
# Dans Base64 URL-safe: _ remplace / et - remplace +
# Donc inversement: _ -> / et @ pourrait être autre chose

# Option 3: Regardons la distribution des caractères
print(f"\nLongueur du contenu: {len(content)}")
print(f"Caractères uniques: {set(content)}")

# Option 4: Peut-être que le message est simplement le texte tel quel ?
# Ou peut-être que c'est un ROT13 ou autre chiffrement simple ?

# Essayons ROT13
import codecs
rot13 = codecs.encode(content, 'rot_13')
print(f"ROT13: {rot13}")

# Essayons de voir si c'est du Base64 standard avec des substitutions différentes
# @ a un code ASCII 64, qui est le caractère '@'
# En Base64 standard, les caractères sont A-Z, a-z, 0-9, +, /
# @ n'est pas dans Base64 standard, donc c'est probablement une substitution

# Peut-être que @ représente un espace ou un autre caractère ?
# Essayons de remplacer @ par espace
modified2 = content.replace('@', ' ')
print(f"Avec @->espace: {modified2}")