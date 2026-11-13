# "doc_ayzagl_mnoj_pmeze_go_ooos"
# Peut-être que c'est une substitution où chaque lettre est décalée d'un certain montant
# basé sur sa position ou une clé

# Ou peut-être que c'est un mot en anglais déguisé
# "doc" -> "doc" (document ou docteur)
# "ayzagl" -> ?
# "mn0j" -> "mnoj" -> ?
# "pm3z3" -> "pmeze" -> ?
# "g0" -> "go"
# "o00s" -> "ooos" -> ?

# Peut-être que c'est "doc_ayzagl_mnoj_pmeze_go_ooos" qui est déjà le flag
# Mais avec le préfixe csaw{...}

# Essayons de voir si c'est une substitution Atbash (a<->z, b<->y, etc.)
def atbash(s):
    result = ""
    for c in s:
        if c.isalpha():
            base = ord('a') if c.islower() else ord('A')
            result += chr(base + (25 - (ord(c) - base)))
        else:
            result += c
    return result

payload = "doc_ayzagl_mnoj_pmeze_go_ooos"
print("Atbash:", atbash(payload))

# Peut-être que c'est une substitution Vigenère avec une clé
# Essayons avec la clé "csaw" ou "finders"

# Ou peut-être que le flag est simplement "csaw{d0c_@yz@gl_mn0j_pm3z3_g0_o00s}"
# et que le payload est déjà le bon format

# Regardons si le payload a un sens en anglais avec une substitution simple
# d0c -> doc
# @yz -> ayz -> maybe "azy" ou "yza"
# @gl -> agl -> maybe "alg" ou "gal"

# Peut-être que c'est "doc_azygal_mnoj_pmeze_go_ooos"
# "doc_azygal" -> "doc_azygal" n'a pas de sens

# Essayons de voir si c'est "doc_ayzagl" -> "doc_ayzagl" -> "doc_ayzagl"
# Peut-être que c'est "doc_ayzagl" = "doc_ayzagl" (un mot inventé)

# Ou peut-être que c'est une phrase en leetspeak:
# "doc ayzagl mnoj pmeze go ooos"
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

# Peut-être que @ = 'a' et 0 = 'o' et 3 = 'e' et le reste est déjà correct
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

# Essayons de voir si c'est une substitution où chaque lettre est décalée de 1
# d->e, o->p, c->d, etc.
payload = "doc_ayzagl_mnoj_pmeze_go_ooos"
result = ""
for c in payload:
    if c.isalpha():
        base = ord('a') if c.islower() else ord('A')
        result += chr((ord(c) - base + 1) % 26 + base)
    else:
        result += c
print("Décalage +1:", result)

result = ""
for c in payload:
    if c.isalpha():
        base = ord('a') if c.islower() else ord('A')
        result += chr((ord(c) - base - 1) % 26 + base)
    else:
        result += c
print("Décalage -1:", result)