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

# Tester l'outil mh_subsetsum_lll
from mh_subsetsum_lll import mh_subsetsum_lll

# Essayer sur le premier ciphertext
target = ciphertexts[0]
print(f"\nPremier ciphertext: {target}")
print(f"Bit length: {target.bit_length()}")

# Appeler l'outil
result = mh_subsetsum_lll(pubkey, target)
print(f"Résultat: {result}")
if result:
    print(f"Longueur du vecteur: {len(result)}")
    # Vérifier
    computed = sum(pubkey[i] for i, b in enumerate(result) if b == 1)
    print(f"Somme vérifiée: {computed}")
    print(f"Correspondance: {computed == target}")