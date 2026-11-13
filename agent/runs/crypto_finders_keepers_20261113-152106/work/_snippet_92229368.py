import re

# Liste des chaînes trouvées dans l'analyse MP4
# On cherche d'autres candidats Base64

# Le texte trouvé était: ZXNucHtkMGNfQHl6QGdsX21uMGpfcG0zejNfZzBfbzAwc30=
# Décodé: esnp{d0c_@yz@gl_mn0j_pm3z3_g0_o00s}

# Peut-être qu'il y a d'autres chaînes Base64 dans le fichier
# Regardons les chaînes qui ressemblent à du Base64

import base64

# Essayons de décoder d'autres chaînes potentielles
# Dans l'analyse, on a vu: "ZXNucHtkMGNfQHl6QGdsX21uMGpfcG0zejNfZzBfbzAwc30="

# Peut-être qu'il y a d'autres chaînes Base64 dans le fichier MP4
# Laissons-moi chercher dans les chaînes trouvées

# Les chaînes trouvées incluent:
# "ZXNucHtkMGNfQHl6QGdsX21uMGpfcG0zejNfZzBfbzAwc30="

# Peut-être qu'il y a d'autres chaînes Base64
# Regardons les chaînes qui commencent par "ZX" ou d'autres motifs Base64

# Dans l'analyse, on a vu:
# [55]     <rdf:li>ZXNucHtkMGNfQHl6QGdsX21uMGpfcG0zejNfZzBfbzAwc30=</rdf:li>

# C'est la seule chaîne Base64 trouvée.

# Peut-être que le flag est le texte déchiffré avec une clé différente
# Essayons de trouver la clé qui transforme "esnp" en "csaw"

ciphertext_prefix = "esnp"
plaintext_prefix = "csaw"

# Vigenère: ciphertext = (plaintext + key) % 26
# Donc: key = (ciphertext - plaintext) % 26

key = []
for c, p in zip(ciphertext_prefix, plaintext_prefix):
    diff = (ord(c) - ord(p)) % 26
    key.append(chr(ord('a') + diff))

print(f"Clé déduite de 'esnp' -> 'csaw': {''.join(key)}")

# La clé est "cant"
# Mais avec "cantfind", on obtient un meilleur résultat

# Peut-être que la clé est "cantfind" et que le texte déchiffré est correct
# Mais le flag soumis a été refusé

# Peut-être que le flag est le texte déchiffré sans substitution Leet
# csaw{y0u_@lw@el_zu0e_hz3w3_e0_o00f}

# Ou peut-être que le flag est le texte après substitution Leet avec corrections
# csaw{you_always_here_to_off}

# Essayons de deviner le flag correct en regardant le texte déchiffré
# csaw{y0u_@lw@el_zu0e_hz3w3_e0_o00f}

# Les mots semblent être:
# y0u -> you
# @lw@el -> always (mais c'est alwael)
# zu0e -> true ?
# hz3w3 -> here ?
# e0 -> to ?
# o00f -> off ?

# Le flag pourrait être: csaw{you_always_true_here_to_off}
# Ou: csaw{you_always_here_to_off}

# Mais le texte déchiffré est: csaw{y0u_@lw@el_zu0e_hz3w3_e0_o00f}
# Après substitution Leet: csaw{you_alwael_zuoe_hzewe_eo_ooof}

# Peut-être que le flag est: csaw{you_always_here_to_off}
# Mais il faut vérifier si c'est le bon flag

# Essayons de soumettre le flag: csaw{you_always_here_to_off}
print("Candidat: csaw{you_always_here_to_off}")