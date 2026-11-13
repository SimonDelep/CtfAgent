# Le payload décodé partiellement est : csaw{d0c_@yz@gl_ma0j_wm3z3_g0_o00s}
# Regardons les caractères à l'intérieur des accolades
inner = "d0c_@yz@gl_ma0j_wm3z3_g0_o00s"

# Peut-être que c'est une substitution où chaque lettre est décalée d'un certain montant
# Essayons de trouver un pattern. Le flag attendu ressemble à quelque chose de lisible.
# "d0c" pourrait être "doc" (0 -> o ?)
# "@yz@gl" pourrait être "something" ?

# Essayons de voir si c'est un ROT13 ou autre
import codecs

print("ROT13:", codecs.encode(inner, 'rot_13'))
print("ROT-13:", codecs.encode(inner, 'rot_13'))

# Essayons différents décalages
for shift in range(1, 26):
    shifted = ''.join(chr((ord(c) - ord('a') + shift) % 26 + ord('a')) if c.islower() else c for c in inner)
    if shift == 1:
        print(f"Shift +{shift}: {shifted}")
    elif shift == 13:
        print(f"Shift +{shift}: {shifted}")

# Peut-être que la substitution est basée sur une clé spécifique
# Regardons les caractères spéciaux : @, _, 0, 3
# @ pourrait être une lettre chiffrée
# 0 pourrait être 'o'
# 3 pourrait être 'e' (leet speak)

# Essayons de décoder en supposant que c'est du leet speak inversé
leet_map = {'0': 'o', '3': 'e', '1': 'i', '4': 'a', '5': 's', '7': 't', '@': 'a', '2': 'z'}
decoded_inner = ""
for c in inner:
    decoded_inner += leet_map.get(c, c)
print(f"Leet decode: {decoded_inner}")