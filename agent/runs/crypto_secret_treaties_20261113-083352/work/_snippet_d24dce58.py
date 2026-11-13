# Approche: pour trouver la trapdoor, on cherche m et w tels que
# private[i] = (pubkey[i] * w) mod n est super-croissante
# 
# Une propriété importante: pour une séquence super-croissante,
# a[i] > sum(a[0:i]) pour tout i
#
# Si on connaît m, alors w = m^{-1} mod n
# Et private[i] = (pubkey[i] * w) mod n
#
# Mais on ne connaît pas n non plus. Cependant, n doit être > max(pubkey)
# et n doit être tel que m * w = 1 mod n.
#
# Une approche: pour chaque m possible, on peut essayer de trouver n tel que
# la séquence (pubkey * w) mod n soit super-croissante.
#
# Mais c'est coûteux. Une autre approche: utiliser le fait que
# pour une séquence super-croissante, le rapport entre éléments consécutifs
# est au moins 2 (en pratique, souvent plus).
#
# Essayons une recherche de m et w avec n fixé à une valeur raisonnable.

# D'abord, trouvons une borne pour n. n doit être > max(pubkey)
# Et n doit être tel que pour le bon m, w = m^{-1} mod n donne une séquence super-croissante.

# Une idée: le ciphertext est la somme des pubkey[i] pour les bits à 1.
# Pour le premier ciphertext, si on suppose que c'est "csaw{", on peut essayer de deviner
# quels bits sont à 1.

# "csaw{" en binaire (72 bits = 9 bytes):
# c = 0x63, s = 0x73, a = 0x61, w = 0x77, { = 0x7b
# En binaire MSB-first:
# 0x63 = 01100011
# 0x73 = 01110011
# 0x61 = 01100001
# 0x77 = 01110111
# 0x7b = 01111011

flag_start = "csaw{"
bits = []
for char in flag_start:
    byte = ord(char)
    for i in range(7, -1, -1):
        bits.append((byte >> i) & 1)

print(f"Bits pour 'csaw{{': {bits}")
print(f"Nombre de bits: {len(bits)}")

# Calculons la somme attendue si le premier ciphertext correspond à "csaw{"
pubkey = []
with open('pubkey.txt', 'r') as f:
    for line in f:
        line = line.strip()
        if line and not line.startswith('#'):
            pubkey.append(int(line))

expected_sum = sum(pubkey[i] for i, b in enumerate(bits) if b == 1)
print(f"Somme attendue pour 'csaw{{': {expected_sum}")
print(f"Premier ciphertext: {1599051655305089304826823929251}")
print(f"Difference: {abs(expected_sum - 1599051655305089304826823929251)}")