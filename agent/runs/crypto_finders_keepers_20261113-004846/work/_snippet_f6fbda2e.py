# La clé [6, 0, 15, 7, 0] donne csaw{ pour les 5 premiers
# Mais après, le résultat n'est pas lisible

# Peut-être que la clé est différente pour chaque caractère
# Ou peut-être que c'est un XOR avec une clé qui change

# Regardons le résultat complet avec la clé répétée
chiffre = "esnp{d0c_@yz@gl_mn0j_pm3z3_g0_o00s}"
cle_base = [6, 0, 15, 7, 0]
resultat = ""
for i, c in enumerate(chiffre):
    k = cle_base[i % len(cle_base)]
    resultat += chr(ord(c) ^ k)

print("Résultat complet:")
print(repr(resultat))
print()
print("Affichage:")
print(resultat)

# Peut-être que le flag est en fait ce résultat, mais avec certains caractères
# qui sont corrects et d'autres non

# Vérifions quels caractères sont imprimables
print("\nCaractères imprimables:")
for i, c in enumerate(resultat):
    if 32 <= ord(c) <= 126:
        print(f"  pos {i}: '{c}'")
    else:
        print(f"  pos {i}: {ord(c)} (non imprimable)")
