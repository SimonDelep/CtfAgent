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
print(f"First target: {ciphertexts[0]}")

# L'outil mh_subsetsum_lll devrait être disponible maintenant
# Essayons de l'appeler via le système d'outils
# Mais d'abord, vérifions si on peut l'importer depuis forge
import sys
import os
forge_path = os.path.join(os.getcwd(), 'forge')
if forge_path not in sys.path:
    sys.path.insert(0, forge_path)

# Listons les fichiers dans forge
print(f"Files in forge: {os.listdir('forge') if os.path.exists('forge') else 'not found'}")