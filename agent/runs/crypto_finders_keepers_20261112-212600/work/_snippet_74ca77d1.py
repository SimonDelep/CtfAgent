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

brut = "esnp{d0c_@yz@gl_mn0j_pm3z3_g0_o00s}"
shifts = [-2, 0, -13, 7]
print("Décalage:", shift_decrypt(brut, shifts))

# Le décalage alphabétique ne fonctionne pas bien car il y a des chiffres et des caractères spéciaux

# Revenons au XOR. Le résultat est "csaw}d?dY@v}FgcXkn?mYpb4|3P`6_`76sr"
# Peut-être que le flag est juste ce résultat, ou qu'il faut le formater différemment

# Regardons si le résultat contient des mots anglais
result = "csaw}d?dY@v}FgcXkn?mYpb4|3P`6_`76sr"
print("\nRésultat:", result)

# Peut-être que le message original est "csaw{...}" et que le contenu est chiffré
# avec une clé qui est différente de [6, 0, 15, 7] ?

# Autre idée : peut-être que le message chiffré est "esnp{...}" et que le message original est "csaw{...}"
# Mais le contenu entre accolades est chiffré avec une clé différente ?

# Essayons de trouver la clé qui transforme le contenu chiffré en un message lisible
# Le contenu chiffré est "d0c_@yz@gl_mn0j_pm3z3_g0_o00s"
# Le contenu attendu devrait être quelque chose de lisible entre les accolades

# Peut-être que le contenu est en base64 ?
import base64
content = "d0c_@yz@gl_mn0j_pm3z3_g0_o00s"
# Remplaçons les caractères non-valides pour base64
content_b64 = content.replace('@', '/')  # @ pourrait être /
print("\nContenu modifié pour base64:", content_b64)

try:
    decoded = base64.b64decode(content_b64 + '==')
    print("Base64 décodé:", decoded)
except Exception as e:
    print("Base64 échec:", e)

# Essayons avec d'autres remplacements
for old, new in [('@', '+'), ('@', '='), ('@', '-')]:
    content_b64 = content.replace('@', new)
    try:
        decoded = base64.b64decode(content_b64 + '==')
        print(f"Base64 avec @{new}: {decoded}")
    except:
        pass