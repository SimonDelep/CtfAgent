# D'abord, essayons de comprendre la structure
# Pour MH, on a: pubkey[i] = (super[i] * w) mod n
# où super est super-croissante

# La clé publique a 72 éléments, donc chaque bloc est 72 bits = 9 bytes
# Le flag est probablement "csaw{...}" 

# Essayons de trouver n d'abord. Dans MH standard, n > sum(super)
# Et w * m = n - 1 (ou similaire)

# Vérifions si n = sum(pubkey) + 1 ou autre
pubkey_sum = 3180674925044265972294667263623
print(f"sum(pubkey) = {pubkey_sum}")

# Le premier ciphertext est 1599051655305089304826823929251
# C'est environ la moitié de sum(pubkey), ce qui est cohérent

# Pour trouver la trapdoor, on cherche w et m tels que:
# super[i] = (pubkey[i] * w) mod n forme une séquence super-croissante
# Et w * m = n - 1 (ou n = w * m + 1)

# Essayons avec mh_trapdoor_search