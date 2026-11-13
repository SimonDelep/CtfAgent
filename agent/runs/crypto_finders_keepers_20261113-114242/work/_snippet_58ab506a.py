import base64

# La chaîne Base64 trouvée dans les métadonnées
b64_string = "ZXNucHtkMGNfQHl6QGdsX21uMGpfcG0zejNfZzBfbzAwc30="
decoded = base64.b64decode(b64_string).decode('utf-8')
print("Décodage Base64:", decoded)

# Comparons avec ce qu'on avait avant
previous = "esnp{d0c_@yz@gl_mn0j_pm3z3_g0_o00s}"
print("Précédent:", previous)
print("Match:", decoded == previous)