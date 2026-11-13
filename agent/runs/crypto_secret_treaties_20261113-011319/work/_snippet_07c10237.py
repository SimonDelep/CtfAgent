# Charger les données
with open('pubkey.txt', 'r') as f:
    lines = [l.strip() for l in f if l.strip() and not l.startswith('#')]
pubkey = [int(x) for x in lines]

with open('ciphertext.txt', 'r') as f:
    lines = [l.strip() for l in f if l.strip() and not l.startswith('#')]
ciphertexts = [int(x) for x in lines]

print(f"pubkey length: {len(pubkey)}")
print(f"First ciphertext: {ciphertexts[0]}")

# Essayer d'appeler subset_sum_solver directement
# L'outil devrait être disponible dans l'environnement
import sys
print("Modules disponibles:", [m for m in sys.modules.keys() if not m.startswith('_')][:20])