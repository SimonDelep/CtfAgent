# Charger les données
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

print(f"Clé publique: {len(pubkey)} éléments")
print(f"Ciphertexts: {len(ciphertexts)} blocs")

# Importer et utiliser l'outil forgé
from mh_solver_v2 import main as mh_solve

# Tester sur le premier ciphertext
target = ciphertexts[0]
print(f"\nPremier ciphertext: {target}")

result = mh_solve({"pubkey": pubkey, "target": target})
print(f"Résultat: {result}")