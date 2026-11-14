# Charger les données exactes
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

# Afficher les valeurs exactes pour le premier appel
print("Pubkey (premier élément):", pubkey[0])
print("Type:", type(pubkey[0]))
print("Ciphertext[0]:", ciphertexts[0])

# Vérifier que nous avons bien 72 éléments
print("Taille pubkey:", len(pubkey))
print("Taille ciphertexts:", len(ciphertexts))