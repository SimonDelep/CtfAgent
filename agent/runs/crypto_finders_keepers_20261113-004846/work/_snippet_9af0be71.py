import base64

encoded = "ZXNucHtkMGNfQHl6QGdsX21uMGpfcG0zejNfZzBfbzAwc30="
decoded = base64.b64decode(encoded).decode('utf-8')
print("Décodage Base64:", decoded)

# La chaîne complète est "esnp{d0c_@yz@gl_mn0j_pm3z3_g0_o00s}"
# On veut convertir "esnp{" en "csaw{"
# Clé XOR: e->c=6, s->s=0, n->a=15, p->w=7, {->{=0? Non, { est 123, { est 123, donc 0

# Attends, vérifions:
# 'esnp{' -> 'csaw{'
# e (101) ^ 6 = 97 = 'c' ✓
# s (115) ^ 0 = 115 = 's' ✓
# n (110) ^ 15 = 97 = 'a' ✓
# p (112) ^ 7 = 119 = 'w' ✓
# { (123) ^ ? = 123 = '{' -> donc 0

# Donc la clé est [6, 0, 15, 7, 0] pour les 5 premiers caractères
# Mais le message complet est "esnp{d0c_@yz@gl_mn0j_pm3z3_g0_o00s}"

# Appliquons la clé XOR répétitivement sur toute la chaîne
key = [6, 0, 15, 7, 0]
result = ""
for i, c in enumerate(decoded):
    k = key[i % len(key)]
    result += chr(ord(c) ^ k)

print("Après XOR avec clé [6,0,15,7,0]:", result)

# Vérifions si c'est lisible