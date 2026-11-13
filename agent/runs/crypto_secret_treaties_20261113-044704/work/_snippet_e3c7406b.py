# Approche: utiliser LLL pour trouver la trapdoor
# La clé publique est: pubkey[i] = (s[i] * w) mod m
# où s est super-increasing

# On peut essayer de trouver w en cherchant un vecteur court
# Construisons un réseau où le vecteur (w, -1) est court

# Une approche: pour chaque paire d'éléments, on a:
# pubkey[i] * w^{-1} ≡ s[i] (mod m)
# pubkey[j] * w^{-1} ≡ s[j] (mod m)

# Donc: pubkey[i] * s[j] ≡ pubkey[j] * s[i] (mod m)

# Mais on ne connaît pas s[i]. On sait que s[i] est petit (super-increasing)

# Autre approche: utiliser le fait que s[i] < m/2 pour tout i (généralement)
# Donc pubkey[i] * w^{-1} mod m = s[i] est petit

# On peut chercher w tel que pubkey[i] * w^{-1} mod m soit petit pour tout i

# Pour trouver w et m, on peut utiliser LLL sur une matrice construite à partir de pubkey

# Approche simplifiée: essayer de trouver m en cherchant un diviseur commun
# ou utiliser LLL directement sur le problème subset-sum

# Pour l'instant, essayons une recherche exhaustive sur w (si m est petit)
# ou utilisons LLL pour trouver un vecteur court

# D'abord, regardons les valeurs de la clé publique
pubkey = []
with open('pubkey.txt', 'r') as f:
    for line in f:
        line = line.strip()
        if line and not line.startswith('#'):
            pubkey.append(int(line))

# Le module m est généralement légèrement supérieur à la somme de la séquence super-increasing
# et w est tel que gcd(w, m) = 1

# Une attaque possible: trouver w en cherchant un vecteur (w, -1) dans le réseau généré par
# les relations linéaires entre les éléments de la clé publique

# Pour Merkle-Hellman, on peut aussi essayer de trouver directement le message
# en utilisant LLL sur la matrice du problème subset-sum

# Construisons la matrice pour LLL:
# On cherche x binaire tel que sum(pubkey[i] * x[i]) = ciphertext
# La matrice est de taille (n+1) x (n+1)

# Mais pour 72 dimensions, LLL pur Python est trop lent
# Essayons une approche différente: branch and bound avec élagage

def solve_subset_sum_branch_bound(pubkey, target, max_depth=None):
    """Résout subset-sum avec branch and bound"""
    n = len(pubkey)
    if max_depth is None:
        max_depth = n
    
    # Trier par ordre décroissant pour mieux élaguer
    indexed_pubkey = sorted(enumerate(pubkey), key=lambda x: -x[1])
    sorted_indices = [x[0] for x in indexed_pubkey]
    sorted_pubkey = [x[1] for x in indexed_pubkey]
    
    # Précalculer les sommes suffixes pour l'élagage
    suffix_sum = [0] * (n + 1)
    for i in range(n - 1, -1, -1):
        suffix_sum[i] = suffix_sum[i + 1] + sorted_pubkey[i]
    
    solution = [None]
    
    def backtrack(idx, current_sum, chosen):
        if solution[0] is not None:
            return True
        if current_sum == target:
            solution[0] = chosen[:]
            return True
        if idx >= n or current_sum > target:
            return False
        if current_sum + suffix_sum[idx] < target:
            return False
        
        # Essayer d'inclure l'élément
        if current_sum + sorted_pubkey[idx] <= target:
            chosen.append(sorted_indices[idx])
            if backtrack(idx + 1, current_sum + sorted_pubkey[idx], chosen):
                return True
            chosen.pop()
        
        # Essayer d'exclure l'élément
        if backtrack(idx + 1, current_sum, chosen):
            return True
        
        return False
    
    backtrack(0, 0, [])
    
    if solution[0] is not None:
        # Convertir en vecteur binaire
        result = [0] * n
        for idx in solution[0]:
            result[idx] = 1
        return result
    return None

# Lire les ciphertexts
ciphertexts = []
with open('ciphertext.txt', 'r') as f:
    for line in f:
        line = line.strip()
        if line and not line.startswith('#'):
            ciphertexts.append(int(line))

print(f"Ciphertexts: {ciphertexts}")

# Essayer de résoudre le premier bloc
print("\nRésolution du premier bloc...")
result = solve_subset_sum_branch_bound(pubkey, ciphertexts[0])
if result:
    print(f"Solution trouvée: {sum(result)} bits à 1")
    print(f"Vérification: {sum(pubkey[i] for i in range(len(pubkey)) if result[i] == 1)}")
else:
    print("Aucune solution trouvée")