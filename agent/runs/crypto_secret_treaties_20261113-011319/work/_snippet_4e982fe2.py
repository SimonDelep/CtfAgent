# Charger les données
with open('pubkey.txt', 'r') as f:
    lines = [l.strip() for l in f if l.strip() and not l.startswith('#')]
pubkey = [int(x) for x in lines]

with open('ciphertext.txt', 'r') as f:
    lines = [l.strip() for l in f if l.strip() and not l.startswith('#')]
ciphertexts = [int(x) for x in lines]

n = len(pubkey)
print(f"n = {n}")
print(f"Premier ciphertext: {ciphertexts[0]}")
print(f"Somme totale de la clé publique: {sum(pubkey)}")
print(f"Densité = n / log2(max(pubkey)) = {n / (len(bin(max(pubkey))) - 2)}")

# Vérifier la densité
import math
max_key = max(pubkey)
print(f"log2(max_key) = {math.log2(max_key)}")
print(f"Densité = {n / math.log2(max_key)}")