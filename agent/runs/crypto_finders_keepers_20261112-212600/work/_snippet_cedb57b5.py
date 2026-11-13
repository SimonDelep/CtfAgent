import base64

# Le message chiffré est "esnp{d0c_@yz@gl_mn0j_pm3z3_g0_o00s}"
# Peut-être que le contenu entre accolades est en base64 ?

content = "d0c_@yz@gl_mn0j_pm3z3_g0_o00s"
print("Contenu:", content)

# Essayons de décoder en base64
try:
    decoded = base64.b64decode(content)
    print("Base64 décodé:", decoded)
except Exception as e:
    print("Base64 échec:", e)

# Peut-être que le contenu est en base64 URL-safe ?
try:
    decoded = base64.urlsafe_b64decode(content + '==')  # Ajouter le padding
    print("Base64 URL-safe décodé:", decoded)
except Exception as e:
    print("Base64 URL-safe échec:", e)

# Autre idée : peut-être que le message original est "csaw{...}" et que le contenu est chiffré
# avec une clé qui est la position ou quelque chose comme ça ?

# Regardons les différences entre le message chiffré et le message attendu
# Message chiffré: esnp{d0c_@yz@gl_mn0j_pm3z3_g0_o00s}
# Message attendu: csaw{...}

# Les différences sont :
# e -> c : -2
# s -> s : 0
# n -> a : -13
# p -> w : +7

# Ces différences sont : -2, 0, -13, +7
# En valeur absolue : 2, 0, 13, 7

# Peut-être que la clé est basée sur ces valeurs ?
# Ou peut-être que la clé est "csaw" XOR "esnp" = [6, 0, 15, 7]

# Essayons de voir si le contenu déchiffré avec la clé [6, 0, 15, 7] donne quelque chose de lisible
# en remplaçant les caractères spéciaux par des underscores ou des espaces

result = "csaw}d?dY@v}FgcXkn?mYpb4|3P`6_`76sr"
print("\nRésultat:", result)

# Remplaçons les caractères non-alphanumériques par des underscores
cleaned = ''.join(c if c.isalnum() or c in ['_', '-'] else '_' for c in result)
print("Nettoyé:", cleaned)

# Peut-être que le flag est "csaw{...}" et que le contenu est "d?dY@v}FgcXkn?mYpb4|3P`6_`76sr"
# Mais ça ne semble pas être un message lisible...

# Autre idée : peut-être que le XOR n'est pas la bonne approche, et qu'il faut utiliser un décalage ?
# Essayons de trouver un décalage qui transforme "esnp" en "csaw"
# e -> c : -2
# s -> s : 0
# n -> a : -13
# p -> w : +7

# Ces décalages ne sont pas constants, donc ce n'est pas un simple ROT-N

# Peut-être que la clé est une séquence de décalages : [-2, 0, -13, 7]
# Et qu'elle s'applique cycliquement ?

def shift_decrypt(ciphertext, shifts):
    result = []
    for i, c in enumerate(ciphertext):
        s = shifts[i % len(shifts)]
        # Décalage alphabétique
        if c.isalpha():
            base = ord('a') if c.islower() else ord('A')
            result.append(chr((ord(c) - base - s) % 26 + base))
        else:
            result.append(c)
    return ''.join(result)

shifts = [-2, 0, -13, 7]
print("\nDécalage:", shift_decrypt(brut, shifts))