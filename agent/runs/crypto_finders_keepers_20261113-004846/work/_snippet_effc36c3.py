# Le résultat est csaw{d0c_@yz@gl_mn0j_pm3z3_g0_o00s}
# Peut-être que c'est le flag, mais il faut le décoder d'une autre manière

# Regardons si le contenu entre les accolades a un sens
content = "d0c_@yz@gl_mn0j_pm3z3_g0_o00s"
print("Contenu entre accolades:", content)

# Peut-être que c'est un autre type de chiffrement
# Ou peut-être que c'est en fait lisible et que je sur-analyse

# Essayons de voir si c'est un ROT13 ou autre
import codecs
print("ROT13:", codecs.encode(content, 'rot_13'))

# Peut-être que c'est un Base64 décodé?
import base64
try:
    decoded = base64.b64decode(content)
    print("Base64 décodé:", decoded)
except:
    print("Base64 échec")

# Peut-être que le flag est simplement csaw{d0c_@yz@gl_mn0j_pm3z3_g0_o00s}
# et qu'il faut le soumettre tel quel

# Mais attendons, regardons si le contenu a un sens
# d0c_@yz@gl_mn0j_pm3z3_g0_o00s
# Peut-être que c'est "doc_...gl_mn0j_pm3z3_g0_o00s"

# Essayons de voir si c'est un XOR avec une autre clé
# ou si c'est un autre schéma

# Autre idée: peut-être que le fichier MP4 contient une image ou un autre flux
# qui a le flag

# Pour l'instant, essayons de soumettre le flag tel quel
flag = "csaw{d0c_@yz@gl_mn0j_pm3z3_g0_o00s}"
print("Flag candidat:", flag)
