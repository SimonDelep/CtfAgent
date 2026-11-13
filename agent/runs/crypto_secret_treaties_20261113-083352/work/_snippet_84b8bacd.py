# Essayons d'utiliser l'outil mh_trapdoor_search
# Mais d'abord, créons les fichiers dans le bon format

# Écrivons la clé publique et les ciphertexts dans des fichiers temporaires
with open('pubkey.txt', 'r') as f:
    lines = [l.strip() for l in f if l.strip() and not l.startswith('#')]
pubkey = [int(x) for x in lines]

with open('ciphertext.txt', 'r') as f:
    lines = [l.strip() for l in f if l.strip() and not l.startswith('#')]
ciphertexts = [int(x) for x in lines]

# Écrivons dans des fichiers au format attendu par les outils
with open('pubkey_mh.txt', 'w') as f:
    for p in pubkey:
        f.write(f"{p}\n")

with open('ciphertext_mh.txt', 'w') as f:
    for c in ciphertexts:
        f.write(f"{c}\n")

print("Fichiers créés")
print(f"pubkey_mh.txt: {len(pubkey)} éléments")
print(f"ciphertext_mh.txt: {len(ciphertexts)} éléments")