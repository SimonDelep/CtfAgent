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

# L'outil mh_subsetsum_lll est forgé, essayons de l'appeler directement
# Il devrait être disponible dans l'environnement
import sys
print("Modules disponibles:", [m for m in sys.modules if 'mh' in m.lower() or 'lll' in m.lower()])