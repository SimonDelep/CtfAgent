# Le ciphertext est: esnp{d0c_@yz@gl_mn0j_pm3z3_g0_o00s}
# Avec la clé cantfind, on obtient: csaw{y0u_@lw@el_zu0e_hz3w3_e0_o00f}

# Regardons les différences entre ce qu'on a et ce qu'on voudrait
# Si on veut "you_always_be_here_to_off" ou similaire

# Les lettres chiffrées sont: d c y z g l m n j p m z g o s
# Avec la clé cantfind, elles deviennent: y o u l w a z u e h z e o o f

# Vérifions:
ciphertext = "esnp{d0c_@yz@gl_mn0j_pm3z3_g0_o00s}"
key = "cantfind"

def vigenere_decrypt(ciphertext, key):
    result = []
    key_idx = 0
    for char in ciphertext:
        if char.isalpha():
            base = ord('A') if char.isupper() else ord('a')
            key_char = key[key_idx % len(key)]
            key_shift = ord(key_char.lower()) - ord('a')
            decrypted = chr((ord(char) - base - key_shift) % 26 + base)
            result.append(decrypted)
            key_idx += 1
        else:
            result.append(char)
    return ''.join(result)

decrypted = vigenere_decrypt(ciphertext, key)
print("Déchiffré:", decrypted)

# Extraire les lettres du contenu déchiffré
content_decrypted = decrypted[5:-1]
decrypted_letters = [c for c in content_decrypted if c.isalpha()]
print("Lettres déchiffrées:", ''.join(decrypted_letters))

# Comparons avec ce qu'on voudrait
# Si le message est "you_always_be_here_to_off", les lettres seraient:
# y o u a l w a y s b e h e r e t o o f f
# Mais on a seulement 15 lettres...

# Peut-être que le message est plus court: "you_always_here" = 13 lettres
# Ou "you_always_be" = 11 lettres

# Regardons ce qu'on a: y o u l w a z u e h z e o o f (15 lettres)
# Cela ne ressemble pas à un message clair

# Essayons de voir si c'est un autre chiffrement
# Peut-être que le message est en fait "you_always_look_here" ou similaire

# Ou peut-être que la clé est différente
# Essayons de trouver la clé qui donnerait "you_always" comme début

# Les 8 premières lettres chiffrées sont: d c y z g l m n
# Si on veut "you_alway" (9 lettres, mais on a 8)...

# Attends, le préfixe "csaw{" utilise aussi la clé!
# Donc les 4 premières lettres "esnp" deviennent "csaw" avec la clé "cant"
# Ensuite "{" n'est pas une lettre, donc la clé continue avec "find" pour le contenu

# Donc pour le contenu, la clé commence à "find" puis "cantfind" etc.
# Vérifions:
print("\nVérification de la clé:")
print("Position 0-3 (esnp -> csaw): clé = cant")
print("Position 4 ({): pas de clé")
print("Position 5+ (contenu): clé continue avec find, puis cantfind...")

# Donc pour le contenu, la clé est: findcantfindcant...
# Les 15 lettres du contenu sont chiffrées avec: findcantfindcantf

# Vérifions:
content_ciph = "d0c_@yz@gl_mn0j_pm3z3_g0_o00s"
content_key = "findcantfindcantf"  # 15 caractères de clé pour 15 lettres
print("\nClé pour le contenu:", content_key)

# Déchiffrons avec cette clé
def vigenere_decrypt_content(ciphertext, key):
    result = []
    key_idx = 0
    for char in ciphertext:
        if char.isalpha():
            base = ord('A') if char.isupper() else ord('a')
            key_char = key[key_idx % len(key)]
            key_shift = ord(key_char.lower()) - ord('a')
            decrypted = chr((ord(char) - base - key_shift) % 26 + base)
            result.append(decrypted)
            key_idx += 1
        else:
            result.append(char)
    return ''.join(result)

# Mais en fait, la clé est continue depuis le début
# Donc pour le contenu, on utilise la clé à partir de la position 4 (après les 4 lettres du préfixe)
# Position 0-3: esnp -> csaw (clé: cant)
# Position 4: { (pas de clé)
# Position 5+: contenu (clé continue: findcantfind...)

# Donc la clé pour le contenu est: findcantfindcantf (15 lettres)
# Vérifions:
print("\nDéchiffré avec clé continue:", decrypted)