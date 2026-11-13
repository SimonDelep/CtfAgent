# Le contenu déchiffré est: d0c_@yz@gl_mn0j_pm3z3_g0_o00s
# Peut-être que c'est un code ou un message en "leet speak" ou avec des substitutions ?

content = "d0c_@yz@gl_mn0j_pm3z3_g0_o00s"

# Essayons de remplacer les chiffres par des lettres
# 0 -> o, 3 -> e, etc.
translation = str.maketrats({
    '0': 'o',
    '3': 'e',
    '@': 'a',  # ou autre
    '_': ' ',  # espace
})

# Mais d'abord, regardons si c'est peut-être un message en anglais avec des substitutions
# d0c_@yz@gl_mn0j_pm3z3_g0_o00s
# Si 0=o, 3=e, @=a, _=espace:
# doc ayz a gl mn0j pm3z3 go o00s
# doc ayz a gl mn0j pm3z3 go o00s

# Essayons différentes substitutions
def substitute(s, mapping):
    result = []
    for c in s:
        result.append(mapping.get(c, c))
    return ''.join(result)

# Mapping possible: 0->o, 3->e, @->a, _->espace
mapping1 = {'0': 'o', '3': 'e', '@': 'a', '_': ' '}
print("Mapping 1 (0->o, 3->e, @->a, _->espace):")
print(substitute(content, mapping1))

# Peut-être que @ est un autre caractère ?
# Essayons @ -> 't' (pour "the"?)
mapping2 = {'0': 'o', '3': 'e', '@': 't', '_': ' '}
print("\nMapping 2 (0->o, 3->e, @->t, _->espace):")
print(substitute(content, mapping2))

# Ou peut-être que c'est du "base64" mais avec un alphabet différent ?
# Regardons si le contenu ressemble à du base64 avec un alphabet personnalisé

# Autre idée: peut-être que le message est simplement "doc at zgl mn0j pm3z3 go o00s" ?
# Ou "doc ayz a gl mn0j pm3z3 go o00s" ?

# Essayons de voir si c'est un anagramme ou un message codé
print(f"\nLongueur: {len(content)}")
print(f"Comptage des caractères:")
from collections import Counter
print(Counter(content))