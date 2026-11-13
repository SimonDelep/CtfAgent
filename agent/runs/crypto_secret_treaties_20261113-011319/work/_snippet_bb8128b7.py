# Charger les données
with open('pubkey.txt', 'r') as f:
    lines = [l.strip() for l in f if l.strip() and not l.startswith('#')]
pubkey = [int(x) for x in lines]

with open('ciphertext.txt', 'r') as f:
    lines = [l.strip() for l in f if l.strip() and not l.startswith('#')]
ciphertexts = [int(x) for x in lines]

# Essayer le subset_sum_solver sur le premier ciphertext
from subset_sum_solver import subset_sum_solver

result = subset_sum_solver(pubkey, ciphertexts[0])
print(f"Résultat: {result}")
if result:
    print(f"Indices sélectionnés: {result[:20]}...")
    # Vérifier
    computed = sum(pubkey[i] for i in result)
    print(f"Somme calculée: {computed}")
    print(f"Ciphertext: {ciphertexts[0]}")
    print(f"Match: {computed == ciphertexts[0]}")