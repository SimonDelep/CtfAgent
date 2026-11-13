import base64

encoded = "ZXNucHtkMGNfQHl6QGdsX21uMGpfcG0zejNfZzBfbzAwc30="
decoded = base64.b64decode(encoded).decode('utf-8')
print(f"Base64 décodé: {decoded}")

# Maintenant analyser la substitution
# esnp{d0c_@yz@gl_mn0j_pm3z3_g0_o00s}
# devrait être csaw{...}
# e->c, s->s, n->a, p->w

# Comparons caractère par caractère
expected_prefix = "csaw{"
actual_prefix = "esnp{"

for i, (a, e) in enumerate(zip(actual_prefix, expected_prefix)):
    print(f"Position {i}: '{a}' devrait être '{e}'")