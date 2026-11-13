payload = "d0c_@yz@gl_mn0j_pm3z3_g0_o00s"

# Remplaçons les caractères non-alphabétiques par des espaces pour voir les lettres
letters_only = "".join(c for c in payload if c.isalpha())
print("Lettres seulement:", letters_only)

# Comptons la fréquence des lettres
from collections import Counter
freq = Counter(letters_only.lower())
print("Fréquence des lettres:", freq)

# Peut-être que c'est un chiffrement de substitution simple
# Essayons de voir si c'est un décalage de chaque lettre d'un certain montant
# par rapport à une phrase anglaise courante

# Si le message est "the_quick_brown_fox_jumps_over_the_lazy_dog" ou quelque chose comme ça
# Essayons de trouver un pattern

# Regardons la longueur
print("Longueur du payload:", len(payload))
print("Nombre de lettres:", len(letters_only))