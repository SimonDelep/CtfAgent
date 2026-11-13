# Lire la clé publique et analyser sa structure
pubkey = []
with open('pubkey.txt', 'r') as f:
    for line in f:
        line = line.strip()
        if line and not line.startswith('#'):
            pubkey.append(int(line))

print(f"Nombre d'éléments: {len(pubkey)}")
print(f"Premiers éléments: {pubkey[:5]}")
print(f"Derniers éléments: {pubkey[-5:]}")

# Vérifier si c'est une séquence super-increasing (chaque élément > somme de tous les précédents)
def is_superincreasing(seq):
    total = 0
    for x in seq:
        if x <= total:
            return False
        total += x
    return True

print(f"Super-increasing: {is_superincreasing(pubkey)}")

# Vérifier le rapport entre éléments consécutifs
ratios = [pubkey[i+1]/pubkey[i] for i in range(min(10, len(pubkey)-1))]
print(f"Ratios des premiers éléments: {ratios}")

# Somme totale
total_sum = sum(pubkey)
print(f"Somme totale de la clé publique: {total_sum}")
print(f"Log2 de la somme: {total_sum.bit_length()}")