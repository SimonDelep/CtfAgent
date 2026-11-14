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

print(f"pubkey length: {len(pubkey)}")
print(f"ciphertexts: {ciphertexts}")

# Tester l'outil sur le premier ciphertext
# On va importer la fonction directement
import sys
sys.path.insert(0, 'forge')
from mh_subsetsum_lll import main as mh_solve

target = ciphertexts[0]
result = mh_solve({"pubkey": pubkey, "target": target, "C": 1})
print(f"Result for first ciphertext: {result}")

# Si résultat est une liste, vérifier
if isinstance(result, list):
    computed = sum(pubkey[i] * result[i] for i in range(len(pubkey)))
    print(f"Computed sum: {computed}")
    print(f"Target: {target}")
    print(f"Match: {computed == target}")