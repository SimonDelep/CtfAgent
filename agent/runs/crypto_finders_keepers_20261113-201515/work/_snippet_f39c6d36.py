ciphertext = "esnp{d0c_@yz@gl_mn0j_pm3z3_g0_o00s}"

def vigenere_decrypt(ciphertext, key):
    result = []
    key_idx = 0
    for c in ciphertext:
        if c.isalpha():
            shift = ord(key[key_idx % len(key)].lower()) - ord('a')
            if c.islower():
                result.append(chr((ord(c) - ord('a') - shift) % 26 + ord('a')))
            else:
                result.append(chr((ord(c) - ord('A') - shift) % 26 + ord('A')))
            key_idx += 1
        else:
            result.append(c)
    return ''.join(result)

# Essayons des clés liées au titre "finders keepers"
keys_to_try = [
    "finders",
    "keepers",
    "finderskeepers",
    "finders_keepers",
    "finderskeepersfinders",  # répéter pour couvrir la longueur
    "finderskeepersfind",
    "finderskeeperskeep",
    "finderskeepersfinderskeepers",
]

for key in keys_to_try:
    result = vigenere_decrypt(ciphertext, key)
    print(f"Clé '{key}': {result}")

# Peut-être que la clé est "finderskeepers" mais appliquée différemment?
# Ou peut-être que c'est une combinaison de "finders" et "keepers"?

# Autre idée : peut-être que le message est "csaw{...}" et que le contenu est différent
# Essayons de deviner le contenu en fonction du titre "finders keepers"
# "finders keepers" est une expression anglaise qui signifie "qui trouve garde"
# Peut-être que le message est lié à ça?

# Essayons de voir si le message déchiffré avec 'cantfindit' est correct mais qu'on doit le formater différemment
result = vigenere_decrypt(ciphertext, "cantfindit")
print(f"\nRésultat avec 'cantfindit': {result}")

# Peut-être que le flag est juste le texte sans le préfixe 'csaw{'?
# Ou peut-être que le message est en fait différent?

# Attends, peut-être que le ciphertext n'est pas 'esnp{...}' mais quelque chose d'autre?
# Re-vérifions le Base64
import base64
b64_ciphertext = "ZXNucHtkMGNfQHl6QGdsX21uMGpfcG0zejNfZzBfbzAwc30="
decoded = base64.b64decode(b64_ciphertext).decode('utf-8')
print(f"Base64 décodé: {decoded}")

# C'est bien 'esnp{d0c_@yz@gl_mn0j_pm3z3_g0_o00s}'

# Peut-être que le message final est 'csaw{you_always_know_where_to_look}' mais qu'on doit soumettre avec le wrapper?
# L'indice dit "without a flag wrapper" - peut-être que ça signifie sans le préfixe 'csaw{'?

# Ou peut-être que le message est différent et qu'on a mal interprété le Leet speak?
# 'y0u_@lw@ys_kn0w_wh3r3_t0_l00k'
# 'y0u' = 'you'
# '@lw@ys' = 'always' (avec @ = a)
# 'kn0w' = 'know'
# 'wh3r3' = 'where'
# 't0' = 'to'
# 'l00k' = 'look'

# Donc 'you_always_know_where_to_look'

# Mais peut-être que le message est en fait 'you_always_know_where_to_look' et qu'on doit soumettre ça?
# Ou peut-être que le message est 'y0u_@lw@ys_kn0w_wh3r3_t0_l00k' (avec le Leet)?

# Essayons de voir si le message est différent en utilisant une autre clé
# Peut-être que la clé est 'cantfind' (sans 'it')?
result = vigenere_decrypt(ciphertext, "cantfind")
print(f"\nClé 'cantfind': {result}")

# Peut-être que la clé est 'cantfindit' mais qu'il faut l'appliquer différemment?
# Ou peut-être que le message est en fait différent?
