import base64

content = "d0c_@yz@gl_mn0j_pm3z3_g0_o00s"

# Essayons de voir si c'est du base64 avec un alphabet personnalisé
# Dans le base64 standard: A-Z, a-z, 0-9, +, /
# Ici nous avons: a-z, 0-9, _, @

# Peut-être que _ remplace + et @ remplace / ?
# Ou l'inverse ?

# Essayons différentes substitutions pour obtenir un base64 valide
substitutions = [
    ('_', '+', '@', '/'),  # _ -> +, @ -> /
    ('_', '/', '@', '+'),  # _ -> /, @ -> +
    ('_', '=', '@', ''),   # _ -> = (padding), @ -> vide
]

for sub1, rep1, sub2, rep2 in substitutions:
    modified = content.replace(sub1, rep1).replace(sub2, rep2)
    # Ajouter le padding nécessaire
    padding = (4 - len(modified) % 4) % 4
    modified_padded = modified + '=' * padding
    try:
        decoded = base64.b64decode(modified_padded)
        print(f"Substitution {sub1}->{rep1}, {sub2}->{rep2}:")
        print(f"  Modifié: {modified_padded}")
        print(f"  Décodé: {decoded}")
        # Essayons de décoder en texte
        try:
            text = decoded.decode('utf-8')
            print(f"  Texte: {text}")
        except:
            print(f"  (binaire)")
    except Exception as e:
        print(f"Substitution {sub1}->{rep1}, {sub2}->{rep2}: Erreur {e}")

# Autre idée: peut-être que le message est en fait "doc at zgl mn0j pm3z3 go o00s" 
# et que c'est un message en "leet speak" ?
# d0c = doc, @ = a, 3 = e, 0 = o
# Donc: doc ayz a gl mn0j pm3z3 go o00s
# Si on remplace: d0c -> doc, @ -> a, 3 -> e, 0 -> o, _ -> espace
# doc ayz a gl mn0j pm3z3 go o00s

# Mais "ayz" n'est pas un mot anglais... peut-être "at" ?
# Si @ = t, alors: doc tyztgl... non plus

# Attends, peut-être que c'est "doc at zgl mn0j pm3z3 go o00s"
# et que "zgl" = "zig" ou "zag" ?
# Ou peut-être que c'est un message en français ?

# Essayons de lire le contenu comme un message en "leet speak"
# d0c = doc (document ?)
# @yz = ? 
# gl = ?
# mn0j = ?
# pm3z3 = ?
# g0 = go
# o00s = oos ?

# Peut-être que c'est "doc at zgl mn0j pm3z3 go o00s" et que c'est un message codé ?
# Ou peut-être que le flag est simplement "d0c_@yz@gl_mn0j_pm3z3_g0_o00s" ?

# Essayons de soumettre le contenu tel quel
print("\n--- Tentative de flag ---")
print(f"Flag possible: csaw{{{content}}}")
print(f"Sans wrapper: {content}")