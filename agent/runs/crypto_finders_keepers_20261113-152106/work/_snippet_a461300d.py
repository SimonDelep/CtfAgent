import base64

encoded = "ZXNucHtkMGNfQHl6QGdsX21uMGpfcG0zejNfZzBfbzAwc30="
decoded = base64.b64decode(encoded).decode('utf-8')
print(f"Base64 décodé: {decoded}")

# Essayons de voir le pattern - le flag devrait commencer par "csaw{"
# "esnp{" -> "csaw{" : e->c (-2), s->s (0), n->a (-13), p->w (+7)... pas cohérent

# Peut-être que c'est un décalage simple sur chaque caractère
# Comparons position par position
expected = "csaw{"
actual = decoded[:5]
print(f"Attendu: {expected}, Obtenu: {actual}")

# Calculons les décalages
for i, (a, e) in enumerate(zip(actual, expected)):
    diff = ord(a) - ord(e)
    print(f"Position {i}: '{a}' -> '{e}' = {diff}")