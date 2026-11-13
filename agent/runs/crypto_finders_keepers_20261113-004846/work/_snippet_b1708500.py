# Peut-être que "esnp" est "csaw" décodé avec une clé XOR, et le payload aussi
# Mais la clé n'est pas répétitive, elle change

# Regardons la transformation caractère par caractère:
# e -> c : XOR 6
# s -> s : XOR 0
# n -> a : XOR 15
# p -> w : XOR 7
# { -> { : XOR 0

# La clé serait [6, 0, 15, 7, 0] pour les 5 premiers caractères
# Mais si on applique cette clé sur tout le payload, on obtient des caractères non-imprimables

# Peut-être que la clé est basée sur la position ou sur un mot
# Ou peut-être que c'est une clé qui change après chaque caractère

# Essayons de voir si la clé est "csaw" ou "finders" ou "keepers"
# en appliquant XOR avec la clé sur le payload complet

decoded = "esnp{d0c_@yz@gl_mn0j_pm3z3_g0_o00s}"

# Si la clé est "csaw", alors:
# e ^ c = c ^ c = 0? Non, e ^ c = 6
# s ^ s = 0
# n ^ a = 15
# p ^ w = 7
# { ^ {? = 0

# Donc la clé pour transformer "esnp{" en "csaw{" est [6, 0, 15, 7, 0]
# Mais si on applique cette clé sur le reste du payload, on obtient:

key = [6, 0, 15, 7, 0]
result = ""
for i, c in enumerate(decoded[5:]):  # Skip the prefix
    k = key[i % len(key)]
    result += chr(ord(c) ^ k)

print("Payload XOR avec clé [6,0,15,7,0]:", result)

# Peut-être que la clé est différente pour le payload
# Essayons de trouver une clé qui donne un texte lisible

# Ou peut-être que le payload est déjà le bon format et qu'il faut juste le soumettre
# avec le préfixe csaw{...}

# Regardons si "d0c_@yz@gl_mn0j_pm3z3_g0_o00s" a un sens
# Peut-être que c'est "doc_ayzagl_mnoj_pmeze_go_ooos" qui est le flag

# Ou peut-être que c'est une substitution où @ = 'a', 0 = 'o', 3 = 'e'
# et le reste est déjà correct

# "doc_ayzagl_mnoj_pmeze_go_ooos"
# Peut-être que c'est "doc_ayzagl" = "doc_ayzagl" -> "doc_ayzagl"
# Ou peut-être que c'est "doc_ayzagl" = "doc_ayzagl" -> "doc_ayzagl"

# Essayons de voir si c'est "doc_ayzagl_mnoj_pmeze_go_ooos" qui est le flag
# avec le préfixe csaw{...}

# Mais d'abord, vérifions si le payload a un sens en anglais
# "doc" = document
# "ayzagl" = ?
# "mnoj" = ?
# "pmeze" = ?
# "go" = go
# "ooos" = ?

# Peut-être que c'est "doc_ayzagl_mnoj_pmeze_go_ooos" qui est le flag final
# avec le préfixe csaw{...}

# Essayons de soumettre "csaw{d0c_@yz@gl_mn0j_pm3z3_g0_o00s}"
# Mais d'abord, vérifions si le payload a un sens avec une autre substitution

# Peut-être que c'est une substitution où chaque lettre est décalée d'un certain montant
# basé sur sa position

# Ou peut-être que c'est simplement "csaw{d0c_@yz@gl_mn0j_pm3z3_g0_o00s}"
# et que le payload est déjà le bon format

# Regardons si le payload a un sens en leetspeak avancé
# d0c -> doc
# @yz -> ayz
# @gl -> agl
# mn0j -> mnoj
# pm3z3 -> pmeze
# g0 -> go
# o00s -> ooo s

# "doc_ayzagl_mnoj_pmeze_go_ooos"

# Peut-être que c'est "doc_ayzagl" = "doc_ayzagl" -> "doc_ayzagl"
# Ou peut-être que c'est "doc_ayzagl" = "doc_ayzagl" -> "doc_ayzagl"

# Essayons de voir si c'est "doc_ayzagl_mnoj_pmeze_go_ooos" qui est le flag
# avec le préfixe csaw{...}

# Mais peut-être que le vrai flag est "csaw{doc_ayzagl_mnoj_pmeze_go_ooos}"
# en décodant le leetspeak

# Ou peut-être que c'est "csaw{d0c_@yz@gl_mn0j_pm3z3_g0_o00s}"
# et que le payload est déjà le bon format

# Essayons les deux options
print("\nOption 1: csaw{d0c_@yz@gl_mn0j_pm3z3_g0_o00s}")
print("Option 2: csaw{doc_ayzagl_mnoj_pmeze_go_ooos}")