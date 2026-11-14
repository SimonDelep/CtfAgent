# Essayons d'appeler l'outil via le système
import subprocess
import json

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

# Écrire les données dans un fichier temporaire pour l'outil
import os
os.makedirs('/tmp/mh_data', exist_ok=True)
with open('/tmp/mh_data/pubkey.json', 'w') as f:
    json.dump(pubkey, f)
with open('/tmp/mh_data/ct.json', 'w') as f:
    json.dump(ciphertexts, f)

print("Données écrites")
print(f"pubkey[0:5]: {pubkey[:5]}")
print(f"ciphertexts: {ciphertexts}")