import numpy as np

# Charger la clé publique
pubkey = []
with open('pubkey.txt', 'r') as f:
    for line in f:
        line = line.strip()
        if line and not line.startswith('#'):
            pubkey.append(int(line))

# Charger les ciphertexts
ciphertexts = []
with open('ciphertext.txt', 'r') as f:
    for line in f:
        line = line.strip()
        if line and not line.startswith('#'):
            ciphertexts.append(int(line))

print(f"Nombre d'éléments de clé publique: {len(pubkey)}")
print(f"Nombre de ciphertexts: {len(ciphertexts)}")
print(f"Premier ciphertext: {ciphertexts[0]}")
print(f"Max pubkey: {max(pubkey)}")
print(f"Min pubkey: {min(pubkey)}")

# Vérifier la taille des bits
# 9 bytes = 72 bits
# Le ciphertext est la somme des éléments de pubkey sélectionnés par les bits
# Chaque élément de pubkey est utilisé si le bit correspondant est 1

# Pour un ciphertext donné, on cherche un vecteur binaire x de longueur 72
# tel que sum(pubkey[i] * x[i]) = ciphertext

# Construction de matrice pour LLL
# On veut trouver x binaire tel que sum(pubkey[i] * x[i]) = target
# On construit une matrice où la dernière colonne est la cible

n = len(pubkey)
target = ciphertexts[0]

# Construction classique : matrice (n+1) x (n+1)
# Les n premières lignes ont 1 sur la diagonale et 0 ailleurs
# La dernière ligne a pubkey[i] et -target

# Alternative : embedding avec une constante C
# Matrice (n+1) x (n+1)
# [ I_n     0  ]
# [ pubkey  C  ]
# où C est une constante d'embedding

# Pour forcer la solution binaire, on peut utiliser C = 1 ou une valeur adaptée

# Essayons avec C = 1 d'abord
C = 1
mat = np.zeros((n+1, n+1), dtype=np.int64)

# Les n premières lignes : identité
for i in range(n):
    mat[i, i] = 1

# Dernière ligne : pubkey et -C*target
for i in range(n):
    mat[n, i] = pubkey[i]
mat[n, n] = -C * target

print(f"Matrice shape: {mat.shape}")
print(f"Dernière ligne (premières 10 valeurs): {mat[n, :10]}")
print(f"Dernière valeur: {mat[n, n]}")
