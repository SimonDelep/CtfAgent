# Essayons l'outil mh_trapdoor_search avec une borne plus élevée
# Mais d'abord, regardons ce que fait cet outil

# L'outil mh_trapdoor_search teste des valeurs de m et w
# Pour Merkle-Hellman, m est généralement petit (la séquence super-croissante)
# et w est l'inverse de m mod n

# Mais peut-être que dans ce challenge, m est plus grand
# Ou peut-être que la séquence super-croissante est générée différemment

# Une autre approche: utiliser LLL pour résoudre le problème subset-sum
# Le problème subset-sum faible densité peut être résolu avec LLL

# Densité = n / log2(max(pubkey)) où n est le nombre d'éléments
import math

n_elements = len(pubkey)
max_pubkey = max(pubkey)
log_max = math.log2(max_pubkey)
density = n_elements / log_max

print(f"Nombre d'éléments: {n_elements}")
print(f"Max pubkey: {max_pubkey}")
print(f"log2(max): {log_max}")
print(f"Densité: {density}")

# Pour LLL, on veut une densité < 1/n pour que ça marche bien
# Ici density = 72 / ~45 = ~1.6, ce qui est > 1, donc LLL direct peut ne pas marcher

# Mais peut-être que le problème est plus simple: la séquence super-croissante
# est générée avec des petits nombres, et on peut la retrouver

# Essayons une recherche plus intelligente de la trapdoor
# En MH, la séquence super-croissante S a S[i] > sum(S[0:i-1])
# Et pubkey[i] = (S[i] * w) mod n

# Si on connaît n, on peut essayer de trouver w tel que (pubkey[i] * w) mod n
# forme une séquence super-croissante

# Mais n est inconnu. Dans MH, n > sum(S), et n est généralement choisi
# comme un nombre premier ou un produit de deux grands nombres

# Une idée: si S est super-croissante, alors S[0] est le plus petit élément
# Et S[i] > sum(S[0:i-1])

# Peut-être que n = sum(pubkey) + 1 n'est pas correct
# Essayons d'autres valeurs de n

# Dans MH, n est généralement > sum(S), et pubkey[i] = (S[i] * w) mod n
# Donc n doit être > max(pubkey)

# Essayons n = sum(pubkey) + k pour différents k
print(f"sum(pubkey) = {sum(pubkey)}")
print(f"max(pubkey) = {max(pubkey)}")