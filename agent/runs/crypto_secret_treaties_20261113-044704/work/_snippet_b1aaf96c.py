# Approche: trouver la trapdoor (w, m) pour Merkle-Hellman
# La clé publique est: pubkey[i] = (s[i] * w) mod m
# où s est super-increasing

# Une attaque possible: trouver m en cherchant un diviseur commun
# ou utiliser LLL pour trouver w

# Pour Merkle-Hellman, on peut aussi essayer de trouver directement le message
# en utilisant le fait que la densité est faible

# D'abord, regardons les propriétés de la clé publique
pubkey = []
with open('pubkey.txt', 'r') as f:
    for line in f:
        line = line.strip()
        if line and not line.startswith('#'):
            pubkey.append(int(line))

# Le module m est généralement légèrement supérieur à la somme de la séquence super-increasing
# et w est tel que gcd(w, m) = 1

# Une propriété: pour tout i, j:
# pubkey[i] * s[j] ≡ pubkey[j] * s[i] (mod m)
# Donc: pubkey[i] * s[j] - pubkey[j] * s[i] ≡ 0 (mod m)

# Mais on ne connaît pas s[i]. On sait que s[i] est petit.

# Autre approche: utiliser LLL pour trouver un vecteur court dans le réseau
# généré par les relations entre les éléments de la clé publique

# Pour trouver w, on peut chercher un vecteur (w, -1) dans le réseau
# Construisons une matrice où chaque ligne correspond à une relation

# Approche simplifiée: essayer de trouver m en cherchant un diviseur commun
# des différences entre les éléments de la clé publique

# Calculons les GCDs des paires d'éléments
import math

# Pour trouver m, on peut chercher un diviseur commun des éléments
# Mais m est généralement plus grand que les éléments individuels

# Une autre approche: utiliser le fait que s[i] < m/2 pour tout i
# Donc pubkey[i] * w^{-1} mod m = s[i] est petit

# On peut chercher w tel que pubkey[i] * w^{-1} mod m soit petit pour tout i

# Pour l'instant, essayons une approche basée sur LLL pour trouver directement le message
# en utilisant une matrice plus petite

# Pour un problème subset-sum de densité faible, LLL peut trouver la solution
# en construisant une matrice de taille (n+1) x (n+1)

# Mais pour 72 dimensions, c'est trop lent en pur Python
# Essayons une approche différente: utiliser le fait que le message est du texte ASCII

# Le message est du texte, donc les bits ont une structure particulière
# On peut utiliser cette information pour guider la recherche

# Pour chaque bloc de 9 bytes (72 bits), on sait que:
# - Les bits correspondent à des caractères ASCII
# - Les caractères ASCII ont le bit de poids fort à 0 (pour le texte standard)
# - Donc les 9 premiers bits (ou les 8 premiers bits par caractère) ont une structure

# En fait, le problème dit "Each 9-byte block became a single number: the sum of the public-key entries selected by that block's bits"
# Donc chaque bloc de 9 bytes = 72 bits est chiffré séparément

# Pour décoder, on doit trouver les 72 bits pour chaque bloc
# Et les 72 bits correspondent à 9 caractères ASCII

# Une approche: utiliser LLL avec une matrice pondérée pour favoriser les solutions avec des bits 0/1
# et qui correspondent à du texte ASCII

# Pour l'instant, essayons une approche simple: branch and bound avec élagage basé sur la structure ASCII

def solve_subset_sum_with_pruning(pubkey, target, max_bits=None):
    """Résout subset-sum avec élagage basé sur la structure du message"""
    n = len(pubkey)
    
    # Trier par ordre décroissant pour mieux élaguer
    indexed_pubkey = sorted(enumerate(pubkey), key=lambda x: -x[1])
    sorted_indices = [x[0] for x in indexed_pubkey]
    sorted_pubkey = [x[1] for x in indexed_pubkey]
    
    # Précalculer les sommes suffixes pour l'élagage
    suffix_sum = [0] * (n + 1)
    for i in range(n - 1, -1, -1):
        suffix_sum[i] = suffix_sum[i + 1] + sorted_pubkey[i]
    
    solution = [None]
    
    def backtrack(idx, current_sum, chosen, num_bits):
        if solution[0] is not None:
            return True
        if current_sum == target:
            solution[0] = chosen[:]
            return True
        if idx >= n or current_sum > target:
            return False
        if current_sum + suffix_sum[idx] < target:
            return False
        
        # Élagage basé sur le nombre de bits
        if max_bits is not None:
            # On ne peut pas avoir plus de max_bits bits à 1
            remaining = n - idx
            if num_bits + remaining < max_bits:
                return False
        
        # Essayer d'inclure l'élément
        if current_sum + sorted_pubkey[idx] <= target:
            chosen.append(sorted_indices[idx])
            if backtrack(idx + 1, current_sum + sorted_pubkey[idx], chosen, num_bits + 1):
                return True
            chosen.pop()
        
        # Essayer d'exclure l'élément
        if backtrack(idx + 1, current_sum, chosen, num_bits):
            return True
        
        return False
    
    # Essayer avec différents nombres de bits
    for num_target_bits in range(30, 50):  # Estimation du nombre de bits à 1
        backtrack(0, 0, [], 0)
        if solution[0] is not None:
            break
    
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

# Essayer de résoudre le premier bloc avec une estimation du nombre de bits
print("\nRésolution du premier bloc...")
# Pour 9 bytes de texte ASCII, on s'attend à environ 9 * 4 = 36 bits à 1 en moyenne
# (chaque caractère ASCII a environ 4 bits à 1 en moyenne)
result = solve_subset_sum_with_pruning(pubkey, ciphertexts[0], max_bits=40)
if result:
    print(f"Solution trouvée: {sum(result)} bits à 1")
    print(f"Vérification: {sum(pubkey[i] for i in range(len(pubkey)) if result[i] == 1)}")
else:
    print("Aucune solution trouvée")