# Charger les données
with open('pubkey.txt', 'r') as f:
    lines = [l.strip() for l in f if l.strip() and not l.startswith('#')]
pubkey = [int(x) for x in lines]

with open('ciphertext.txt', 'r') as f:
    lines = [l.strip() for l in f if l.strip() and not l.startswith('#')]
ciphertexts = [int(x) for x in lines]

print(f"pubkey length: {len(pubkey)}")
print(f"ciphertexts: {ciphertexts}")
print(f"First ciphertext: {ciphertexts[0]}")

# Tester le subset_sum_solver
from tools import subset_sum_solver

result = subset_sum_solver(pubkey, ciphertexts[0])
print(f"Result: {result}")