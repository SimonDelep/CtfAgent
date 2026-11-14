# Essayer de voir si '2_5t3@1_' est le résultat d'un XOR avec une clé simple
target = b'2_5t3@1_'

# Peut-être que le flag est 'csaw{...}' et '2_5t3@1_' est le contenu
# csaw{ = 6 caractères, 2_5t3@1_ = 8 caractères
# Donc le format serait csaw{2_5t3@1_}

# Vérifions les longueurs
print(f"Longueur de '2_5t3@1_': {len('2_5t3@1_')}")
print(f"Longueur de 'csaw{{}}': {len('csaw{}')}")

# Si le flag est 'csaw{2_5t3@1_}', la longueur totale est 6 + 8 = 14 caractères
print(f"Longueur de 'csaw{{2_5t3@1_}}': {len('csaw{2_5t3@1_}')}")

# Peut-être que '2_5t3@1_' est une substitution de 'csaw{...}'
# Regardons les différences ASCII
print("\nComparaison ASCII:")
flag_content = '2_5t3@1_'
expected = 'csaw{...}'  # 8 caractères attendus

# 'csaw{...}' n'a pas 8 caractères, donc ce n'est pas une substitution directe
# Peut-être que le contenu du flag est '2_5t3@1_' et le format est csaw{2_5t3@1_}

# Ou peut-être que '2_5t3@1_' est une forme de leet speak
# 2 -> c? 5 -> s? t -> a? 3 -> w? @ -> {? 1 -> }? _ -> ?
# 2_5t3@1_ = c_s_a_w{1_ ? Pas clair

# Essayons de soumettre 'csaw{2_5t3@1_}'
print(f"\nFlag à soumettre: csaw{{2_5t3@1_}}")