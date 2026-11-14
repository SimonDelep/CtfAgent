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

# Le ciphertext a 35 caractères, dont 28 sont alphabétiques (en comptant les lettres dans le préfixe et le corps)
# 'esnp{' = 4 lettres + 1 symbole
# 'd0c_@yz@gl_mn0j_pm3z3_g0_o00s' = beaucoup de lettres

# Comptons les lettres dans le ciphertext
letters_in_ciphertext = [c for c in ciphertext if c.isalpha()]
print(f"Nombre de lettres dans le ciphertext: {len(letters_in_ciphertext)}")
print(f"Lettres: {''.join(letters_in_ciphertext)}")

# Le préfixe 'esnp' a 4 lettres, donc la clé doit décaler 'esnp' en 'csaw'
# 'e' -> 'c' : décalage de -2 (ou +24)
# 's' -> 's' : décalage de 0
# 'n' -> 'a' : décalage de -13 (ou +13)
# 'p' -> 'w' : décalage de +7

# Donc les premiers décalages sont: 24, 0, 13, 7 (en valeur positive)
# En valeur négative (pour le déchiffrement): -2, 0, -13, +7

# Pour le déchiffrement, on soustrait le décalage de la clé
# Donc si 'e' -> 'c', alors (ord('e') - ord('a') - shift) % 26 = ord('c') - ord('a')
# (4 - shift) % 26 = 2
# shift = 2 (ou 28, etc.)

# Vérifions:
# 'e' (4) - 2 = 2 = 'c' ✓
# 's' (18) - 0 = 18 = 's' ✓
# 'n' (13) - 13 = 0 = 'a' ✓
# 'p' (15) - 7 = 8 = 'i'... attendons, 'p' -> 'w'
# 'p' (15) - shift = 22 ('w')
# 15 - shift = 22 (mod 26)
# shift = 15 - 22 = -7 = 19 (mod 26)

# Donc les décalages pour 'csaw' sont: 2, 0, 13, 19

# La clé 'cantfindit' donne:
# 'c' = 2, 'a' = 0, 'n' = 13, 't' = 19
# Donc les 4 premiers caractères de la clé sont 'cant' qui correspondent aux décalages 2, 0, 13, 19!

# Vérifions:
key = "cantfindit"
for i, c in enumerate("esnp"):
    shift = ord(key[i].lower()) - ord('a')
    decrypted = chr((ord(c) - ord('a') - shift) % 26 + ord('a'))
    print(f"'{c}' - '{key[i]}' (shift {shift}) -> '{decrypted}'")

# Donc la clé 'cantfindit' est correcte pour le préfixe 'csaw'
# Le problème est peut-être que le message final est différent?

# Peut-être que le message est en fait 'csaw{you_always_know_where_to_look}' et qu'on doit soumettre avec le wrapper?
# Ou peut-être que le message est différent?

# Essayons de voir si le message est en fait le Leet speak converti en texte normal
# 'y0u_@lw@ys_kn0w_wh3r3_t0_l00k' -> 'you_always_know_where_to_look'

# Mais on a déjà essayé ça...

# Peut-être que le message est différent et qu'on doit trouver une autre interprétation?
# L'indice 'engine=jc' pourrait être une indication que le message est encodé d'une manière spécifique?

# 'jc' pourrait être 'Jeu de Caractères' mais peut-être que c'est une indication que le message est en fait différent?

# Autre idée : peut-être que le message est 'csaw{finders_keepers}' ou quelque chose comme ça?
# Essayons de voir quelle clé donnerait 'csaw{finders_keepers}'

target = "csaw{finders_keepers}"
# On veut trouver la clé qui transforme 'esnp{d0c_@yz@gl_mn0j_pm3z3_g0_o00s}' en 'csaw{finders_keepers}'

# Pour chaque lettre, on calcule le décalage nécessaire
def find_key(ciphertext, plaintext):
    key = []
    c_idx = 0
    for p in plaintext:
        if p.isalpha():
            c = ciphertext[c_idx]
            shift = (ord(c.lower()) - ord('a') - (ord(p.lower()) - ord('a'))) % 26
            key.append(chr(shift + ord('a')))
            c_idx += 1
        else:
            c_idx += 1
    return ''.join(key)

# Essayons avec 'csaw{finders_keepers}'
key_candidate = find_key(ciphertext, "csaw{finders_keepers}")
print(f"\nClé pour 'csaw{{finders_keepers}}': {key_candidate}")

# Essayons avec 'csaw{you_always_know_where_to_look}'
key_candidate2 = find_key(ciphertext, "csaw{you_always_know_where_to_look}")
print(f"Clé pour 'csaw{{you_always_know_where_to_look}}': {key_candidate2}")

# La clé pour 'csaw{you_always_know_where_to_look}' devrait être 'cantfindit'
# Vérifions:
print(f"\nVérification: {key_candidate2}")
