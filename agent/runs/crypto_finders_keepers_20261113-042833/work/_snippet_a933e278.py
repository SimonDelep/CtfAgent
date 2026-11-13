import base64

content = "d0c_@yz@gl_mn0j_pm3z3_g0_o00s"
print(f"Contenu: {content}")

# Essayons de voir si c'est un décodage Base64
# Mais d'abord, remplaçons les caractères spéciaux par des caractères Base64 valides
# @ pourrait être + ou /
# _ pourrait être - ou _

# Essayons différentes substitutions
substitutions = [
    ("@", "+"),
    ("@", "/"),
    ("_", "-"),
    ("_", "+"),
]

for sub_char, repl in substitutions:
    modified = content.replace(sub_char, repl)
    print(f"Remplacement {sub_char} -> {repl}: {modified}")
    try:
        # Essayer de décoder en Base64
        decoded = base64.b64decode(modified + '==').decode('utf-8', errors='ignore')
        print(f"  Base64 décodé: {decoded}")
    except:
        pass

# Peut-être que c'est un décalage sur les caractères alphanumériques seulement
print("\nTest de décodage avec substitution de caractères:")
# @ est ASCII 64, _ est 95
# Peut-être que @ devrait être un espace ou un autre caractère

# Essayons de remplacer @ par un espace
modified = content.replace("@", " ")
print(f"@ -> espace: {modified}")

# Essayons de remplacer @ par un underscore
modified = content.replace("@", "_")
print(f"@ -> _: {modified}")

# Peut-être que c'est un décalage de 1 sur les lettres
print("\nTest décalage -1 sur les lettres:")
decoded = ""
for c in content:
    if c.isalpha():
        base = ord('A') if c.isupper() else ord('a')
        decoded += chr((ord(c) - base - 1) % 26 + base)
    else:
        decoded += c
print(decoded)