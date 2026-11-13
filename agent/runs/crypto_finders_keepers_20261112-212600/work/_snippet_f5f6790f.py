# Le contenu déchiffré est: d0c_@yz@gl_mn0j_pm3z3_g0_o00s
content = "d0c_@yz@gl_mn0j_pm3z3_g0_o00s"

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

# Essayons de remplacer @ par 'a' et voir si ça donne un mot anglais
mapping3 = {'0': 'o', '3': 'e', '@': 'a', '_': ''}  # _ comme séparateur vide
print("\nMapping 3 (0->o, 3->e, @->a, _->vide):")
print(substitute(content, mapping3))

# Peut-être que le message est en fait "doc_ayz_gl_mn0j_pm3z3_g0_o00s" et qu'il faut lire différemment ?
# Ou peut-être que c'est un hash ou un code ?

# Essayons de voir si c'est du base32 ou base64 avec padding
import base64
# Enlevez les underscores et remplacez @ par quelque chose
modified = content.replace('_', '').replace('@', 'A')
print(f"\nSans underscores, @->A: {modified}")
try:
    # Base64 nécessite un multiple de 4
    padding = (4 - len(modified) % 4) % 4
    decoded = base64.b64decode(modified + '=' * padding)
    print(f"Décodé Base64: {decoded}")
except Exception as e:
    print(f"Erreur Base64: {e}")