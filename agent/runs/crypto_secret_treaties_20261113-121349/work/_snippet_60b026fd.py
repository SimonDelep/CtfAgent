# Analyser la clé publique pour trouver des patterns
with open('pubkey.txt', 'r') as f:
    lines = [l.strip() for l in f if l.strip() and not l.startswith('#')]
pubkey = [int(l) for l in lines]

# Vérifier si la clé publique a des propriétés particulières
print("Analyse de la clé publique:")
print(f"Min: {min(pubkey)}")
print(f"Max: {max(pubkey)}")
print(f"Somme: {sum(pubkey)}")

# Trier et voir les ratios
sorted_pubkey = sorted(pubkey)
print("\nÉléments triés (premiers 10):")
for i, v in enumerate(sorted_pubkey[:10]):
    print(f"  {i}: {v}")

print("\nRatios entre éléments consécutifs triés:")
for i in range(1, min(10, len(sorted_pubkey))):
    ratio = sorted_pubkey[i] / sorted_pubkey[i-1]
    print(f"  {sorted_pubkey[i-1]} -> {sorted_pubkey[i]}: ratio = {ratio:.2f}")

# Vérifier si c'est déjà super-increasing (trié)
running_sum = 0
is_super = True
for v in sorted_pubkey:
    if v <= running_sum:
        is_super = False
        break
    running_sum += v

print(f"\nLa clé publique triée est-elle super-increasing? {is_super}")