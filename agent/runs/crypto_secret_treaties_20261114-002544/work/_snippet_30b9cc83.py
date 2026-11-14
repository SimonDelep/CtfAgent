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

# Appeler l'outil mh_lll_solver
from mh_lll_solver import main as mh_solve

result = mh_solve({"pubkey": pubkey, "target": ciphertexts[0], "C": 1})
print("Résultat pour C=1:")
print(result)