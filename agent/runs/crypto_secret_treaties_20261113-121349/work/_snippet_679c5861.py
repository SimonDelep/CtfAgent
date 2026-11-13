# Approche LLL améliorée pour Merkle-Hellman
# La matrice standard est:
# [ 1  0  ...  0  -b[0] ]
# [ 0  1  ...  0  -b[1] ]
# [ ...           ...   ]
# [ 0  0  ...  1  -b[n-1] ]
# [ 0  0  ...  0   C     ]
#
# Mais pour Merkle-Hellman, on veut trouver x tel que sum(x[i] * b[i]) = C
# où x[i] est 0 ou 1

# Une meilleure approche: utiliser la matrice où on cherche un vecteur (x, 1)
# tel que sum(x[i] * b[i]) - C = 0

# Construisons une matrice de dimension (n+1) x (n+1)
# Les n premières lignes ont un 1 sur la diagonale et -b[i] dans la dernière colonne
# La dernière ligne a C dans la dernière colonne

# Mais pour que LLL trouve le bon vecteur, on doit pondérer correctement
# On utilise une approche où on cherche un vecteur court dans le réseau

import math

pubkey = [
65363128684447571132776241699,
11274630258057967396026665723,
60559222278375482447330083794,
70238185910865550789020602007,
78077025115892356117353286514,
68689714170530501420950259719,
29127755965063579516555824180,
32796713726379898017330479743,
45519033311461958996652579847,
59481922183281857526171199789,
55495084400556906381284478613,
14576717810183300603139843389,
68589281729516899808716443746,
20296909478473654757282621208,
30537953005493837032599666770,
50700906734420621772366528392,
58720389817577647385263517768,
14929982408329983159745130411,
78957868028931941741179820628,
31015553887459374066166570979,
6479387240029285522500789709,
44834052244814211323002768825,
68880768174885210134417155701,
70728065516536734229876378887,
19940352925118383021332476475,
11926610039430690869353776248,
44284085306881906513505933290,
65961141103798053905550707203,
79222330366488147095589071397,
57716218939764421264346243444,
7143427741922311277425019977,
40102124774314571307421209726,
31106346336357167193152859646,
9869211918329061407583377438,
23696943552216795845779539234,
57055944207555268510811881306,
3327580670445191612826287616,
10613681056449056256265359590,
59950266048603035641387473838,
58927069738258076769247034796,
64441245461962817349401724273,
49297856532179662020349932300,
45182819049805987851607519281,
35526859738167888566962688623,
69627835129445026186765372626,
42091939332905056814598857452,
13191888117017754559626998031,
45745228201887970683682373391,
62110476246079115246893565460,
34936923235681473070158040183,
21488885432536346192206522870,
71644808849324143031304224752,
68376445195906361888347719926,
51783851937617327120469134628,
65557742112975106585661516908,
54063485202872162576322297308,
74075528359043450527980626626,
42713815274261871699013795581,
67529400689171140706681990106,
21066253853172746373456494821,
56109555611748530333568577993,
18657428926348050402028051389,
13281943995839590735434938781,
41966820243972970004685470533,
42715438945182202722984178323,
58189724253003705746237182254,
74448304789798298732507599455,
10158206024125176882906547212,
45737872490388506855671491388,
52889203964129866973885109,
50666903728700094028720106297,
51522962071682837162170650478
]

ciphertexts = [
1599051655305089304826823929251,
1797746206330633665893908016565,
1661865493958450122592244546366,
1514497994514640235239498547775,
1612686994707484946937928105122,
1910510829453185702573591325325,
994664683904375893078154622717
]

n = len(pubkey)

# Pour Merkle-Hellman, l'attaque LLL fonctionne mieux quand la densité est faible
# Densité = n / log2(max(b))
# Ici, max(b) ≈ 8e13, log2(8e13) ≈ 46, donc densité ≈ 72/46 ≈ 1.56
# C'est > 1, donc l'attaque LLL directe peut ne pas fonctionner

# Une autre approche: trouver la trapdoor (w, m)
# On sait que b[i] = (a[i] * w) mod m
# Donc b[i] * w^{-1} ≡ a[i] (mod m)

# Si on peut trouver m, alors on peut calculer a[i] = (b[i] * w^{-1}) mod m
# Et vérifier si a est super-croissante

# Une astuce: si on prend deux éléments b[i] et b[j], alors
# b[i] * w^{-1} ≡ a[i] (mod m)
# b[j] * w^{-1} ≡ a[j] (mod m)
# Donc b[i] * a[j] ≡ b[j] * a[i] (mod m)
# Donc m divise (b[i] * a[j] - b[j] * a[i])

# Mais on ne connaît pas a[i]...

# Essayons une approche différente: utiliser le fait que pour une séquence super-croissante,
# a[i] > sum(a[0..i-1])
# Donc a[i] / sum(a[0..i-1]) > 1

# Pour Merkle-Hellman, souvent m est choisi comme un nombre premier ou proche d'une puissance de 2
# Et w est choisi tel que gcd(w, m) = 1

# Une approche pratique: essayer de trouver m en cherchant un nombre tel que
# quand on calcule (b[i] * w^{-1}) mod m pour différents w, on obtient une séquence super-croissante

# Mais c'est coûteux...

# Essayons une approche par recherche de m en utilisant le fait que
# m doit être > sum(a) et m > max(b)

# Pour une séquence super-croissante de 72 éléments, sum(a) est dominé par le dernier élément
# Si a[i] ≈ 2^i * a[0], alors sum(a) ≈ 2^72 * a[0]

# Mais on ne connaît pas a[0]...

# Une autre idée: utiliser le fait que b[i] = (a[i] * w) mod m
# Donc b[i] < m pour tout i
# Donc m > max(b) = 79222330366488147095589071397

# Et m > sum(a)
# Si a est super-croissante, sum(a) < 2 * a[71] (le dernier élément)
# Donc m > 2 * a[71]

# Mais a[71] = (b[71] * w^{-1}) mod m
# Donc a[71] < m
# Donc sum(a) < 2 * m

# En fait, pour Merkle-Hellman, on choisit m > sum(a), donc m peut être juste au-dessus de sum(a)

# Essayons de trouver m en cherchant autour de la somme totale de la clé publique
# Mais la somme totale est 3.18e30, ce qui est énorme

# Une approche différente: utiliser LLL pour trouver directement le vecteur binaire
# en construisant une matrice où le vecteur solution est très court

# La matrice standard pour subset-sum est:
# [ 2*b[0]  2*b[1]  ...  2*b[n-1]  C ]
# [   1       0     ...     0      0 ]
# [   0       1     ...     0      0 ]
# [  ...    ...    ...    ...    ... ]
# [   0       0     ...     1      0 ]
#
# Le vecteur solution est (x[0], x[1], ..., x[n-1], -1) où x[i] est 0 ou 1

# Mais cette matrice est de dimension (n+1) x (n+1)

# Essayons avec une pondération différente
print("Construction de la matrice LLL pour subset-sum...")
print(f"n = {n}")

# Pour que LLL fonctionne, on doit avoir une densité faible
# Densité = n / log2(max(b))
max_b = max(pubkey)
log_max_b = max_b.bit_length()
density = n / log_max_b
print(f"Densité = {density:.4f} (n={n}, log2(max_b)={log_max_b})")

# Si densité < 0.94, LLL devrait trouver la solution
# Ici densité ≈ 1.56, ce qui est > 1, donc LLL direct peut échouer

# Mais on peut essayer quand même avec une matrice bien pondérée