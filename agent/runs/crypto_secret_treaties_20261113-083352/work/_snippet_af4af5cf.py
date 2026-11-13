# Lisons la clé publique et les ciphertexts
pubkey = []
with open('pubkey.txt', 'r') as f:
    for line in f:
        line = line.strip()
        if line and not line.startswith('#'):
            pubkey.append(int(line))

ciphertexts = []
with open('ciphertext.txt', 'r') as f:
    for line in f:
        line = line.strip()
        if line and not line.startswith('#'):
            ciphertexts.append(int(line))

print(f"Nombre d'éléments pubkey: {len(pubkey)}")
print(f"Nombre de ciphertexts: {len(ciphertexts)}")
print(f"Premier ciphertext: {ciphertexts[0]}")
print(f"Clé publique (premiers 10): {pubkey[:10]}")

# Pour Merkle-Hellman, la clé publique est: pubkey[i] = (private[i] * m) mod n
# où private est super-croissante
# La trapdoor est (w, m) où w = m^{-1} mod n
# Pour décrypter: c' = (c * w) mod n, puis résoudre subset-sum avec private

# La séquence super-croissante a la propriété: a[i] > sum(a[0:i])
# Donc le maximum de la séquence privée doit être > somme de tous les autres

# Essayons de trouver n (le module). n doit être > somme de tous les éléments de la séquence privée
# Et n doit être tel que m * w = 1 mod n

# Une approche: pour chaque m possible, calculer w = m^{-1} mod n pour chaque n possible
# et vérifier si la séquence résultante est super-croissante

# Mais d'abord, estimons la taille de n. La somme maximale possible est quand tous les bits sont 1
# c_max = sum(pubkey)
print(f"Somme de la clé publique: {sum(pubkey)}")
print(f"Max de la clé publique: {max(pubkey)}")