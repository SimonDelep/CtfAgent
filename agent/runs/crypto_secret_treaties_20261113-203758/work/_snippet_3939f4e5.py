# Lisons les données et testons l'outil mh_subsetsum_solver
import sys
sys.path.insert(0, '/usr/local/lib/python3.12/dist-packages')

# Lire la clé publique
pubkey = []
with open('pubkey.txt', 'r') as f:
    for line in f:
        line = line.strip()
        if line and not line.startswith('#'):
            pubkey.append(int(line))

# Lire les ciphertexts
ciphertexts = []
with open('ciphertext.txt', 'r') as f:
    for line in f:
        line = line.strip()
        if line and not line.startswith('#'):
            ciphertexts.append(int(line))

print(f"Clé publique: {len(pubkey)} éléments")
print(f"Premier élément: {pubkey[0]}")
print(f"Nombre de ciphertexts: {len(ciphertexts)}")
print(f"Premier ciphertext: {ciphertexts[0]}")

# Vérifier la densité
n = len(pubkey)
bits_per_block = 72
density = bits_per_block / n
print(f"Densité: {density}")

# Vérifier que les ciphertexts sont dans le bon ordre de grandeur
max_sum = sum(pubkey)
print(f"Somme max possible: {max_sum}")
print(f"Ratio ct/max: {ciphertexts[0]/max_sum}")