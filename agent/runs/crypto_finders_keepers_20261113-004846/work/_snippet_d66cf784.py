cipher = "esnp{d0c_@yz@gl_mn0j_pm3z3_g0_o00s}"

# Si on suppose que le flag est de la forme csaw{...} et qu'il contient des mots anglais
# on peut essayer de deviner la clé XOR en regardant les différences

# La clé pour le préfixe est [6, 0, 15, 7, 0]
# Peut-être que la clé est "csaw" mais appliquée différemment

# Autre idée : peut-être que c'est un XOR avec une clé qui est le mot "csaw" répété,
# mais en commençant par une position différente

# Ou peut-être que la clé est un mot différent

# Essayons de trouver la clé en supposant que le flag contient "the" ou "flag"
# ou d'autres mots communs

# Si on suppose que le flag est "csaw{...}" et qu'il contient des mots anglais,
# on peut essayer de deviner la clé XOR

# Regardons la chaîne chiffrée et essayons de trouver un pattern
print("Chaîne chiffrée:", cipher)
print("Longueur:", len(cipher))

# Peut-être que la clé est "finders" ou "keepers" ou un mot lié au challenge
# Essayons de trouver la clé en XORant avec des mots communs

def xor_decrypt(cipher_text, key):
    result = []
    for i, c in enumerate(cipher_text):
        result.append(chr(ord(c) ^ key[i % len(key)]))
    return ''.join(result)

# Clé "finders"
print("Clé 'finders':", xor_decrypt(cipher, "finders"))

# Clé "keepers"
print("Clé 'keepers':", xor_decrypt(cipher, "keepers"))

# Clé "finderskeepers"
print("Clé 'finderskeepers':", xor_decrypt(cipher, "finderskeepers"))

# Clé "hidden"
print("Clé 'hidden':", xor_decrypt(cipher, "hidden"))

# Clé "message"
print("Clé 'message':", xor_decrypt(cipher, "message"))

# Clé "video"
print("Clé 'video':", xor_decrypt(cipher, "video"))

# Clé "mp4"
print("Clé 'mp4':", xor_decrypt(cipher, "mp4"))

# Clé "base64"
print("Clé 'base64':", xor_decrypt(cipher, "base64"))

# Clé "xmp"
print("Clé 'xmp':", xor_decrypt(cipher, "xmp"))

# Clé "adobe"
print("Clé 'adobe':", xor_decrypt(cipher, "adobe"))

# Clé "canva"
print("Clé 'canva':", xor_decrypt(cipher, "canva"))
