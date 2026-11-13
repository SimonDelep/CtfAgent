import base64

content = "d0c_@yz@gl_mn0j_pm3z3_g0_o00s"

# Essayons base32
# Base32 utilise A-Z et 2-7, donc pas de chiffres 0, 1, 8, 9
# Notre contenu a des 0, 3, donc ce n'est pas du base32 standard

# Essayons base64 avec l'alphabet standard mais en traitant _ et @ comme des caractères valides
# Peut-être que c'est du base64 URL-safe où _ remplace / et - remplace +
# Mais nous avons @, pas -

# Autre idée: peut-être que le contenu est déjà le message final, et qu'il faut juste le soumettre ?
# Ou peut-être que c'est un message en "leet speak" qui doit être lu tel quel ?

# Essayons de voir si le contenu est un anagramme d'un message en anglais
from collections import Counter

# Comptons les lettres (en ignorant les chiffres et symboles)
letters_only = ''.join(c for c in content if c.isalpha())
print(f"Lettres seulement: {letters_only}")
print(f"Comptage: {Counter(letters_only)}")

# Essayons de voir si c'est un message en "rot" ou "caesar" cipher
def rot_n(s, n):
    result = []
    for c in s:
        if c.isalpha():
            base = ord('a') if c.islower() else ord('A')
            result.append(chr((ord(c) - base + n) % 26 + base))
        else:
            result.append(c)
    return ''.join(result)

# Essayons tous les décalages ROT
print("\nTous les décalages ROT:")
for i in range(26):
    decoded = rot_n(content, i)
    print(f"ROT{i}: {decoded}")