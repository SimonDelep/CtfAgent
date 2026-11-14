import sys
sys.path.insert(0, '/home/etudiantelambda/Documents/CSAW_LLM_2026-BTN-DLP/CtfAgent/agent/runs/crypto_secret_treaties_20261113-203758/forge')

# Importer l'outil
import mh_subsetsum_solver

# Lire les données
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
print(f"Nombre de ciphertexts: {len(ciphertexts)}")

# Essayer de résoudre le premier bloc
ct = ciphertexts[0]
print(f"\nTentative avec ciphertext: {ct}")

# Tester la méthode lagarias
result = mh_subsetsum_solver.solve_lagarias(pubkey, ct)
print(f"Résultat lagarias: {result}")
if result is not None:
    print(f"Longueur: {len(result)}")
    print(f"Somme: {sum(result)}")