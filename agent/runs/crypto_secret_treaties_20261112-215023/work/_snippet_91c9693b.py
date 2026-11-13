# Implémentation de LLL en Python pur
import math

def gram_schmidt(B):
    """Calcul de la base de Gram-Schmidt pour une base B"""
    n = len(B)
    m = len(B[0])
    B_star = [[0.0] * m for _ in range(n)]
    mu = [[0.0] * n for _ in range(n)]
    
    for i in range(n):
        for j in range(m):
            B_star[i][j] = B[i][j]
    
    for i in range(n):
        for j in range(i):
            s = sum(B_star[i][k] * B_star[j][k] for k in range(m))
            mu[i][j] = s / sum(B_star[j][k] * B_star[j][k] for k in range(m)) if sum(B_star[j][k] * B_star[j][k] for k in range(m)) != 0 else 0
            for k in range(m):
                B_star[i][k] -= mu[i][j] * B_star[j][k]
    
    return B_star, mu

def lll(B, delta=0.99):
    """LLL réduction de base"""
    n = len(B)
    m = len(B[0])
    
    # Convertir en float pour les calculs
    B = [[float(x) for x in row] for row in B]
    
    B_star, mu = gram_schmidt(B)
    
    k = 1
    while k < n:
        # Condition de Lovasz
        norm_k_minus_1 = sum(B_star[k-1][j] ** 2 for j in range(m))
        norm_k = sum(B_star[k][j] ** 2 for j in range(m))
        
        if delta * norm_k_minus_1 > norm_k:
            # Échange
            B[k-1], B[k] = B[k], B[k-1]
            B_star, mu = gram_schmidt(B)
            k = max(1, k - 1)
        else:
            # Condition de taille
            for j in range(k):
                if abs(mu[k][j]) > 0.5:
                    q = round(mu[k][j])
                    B[k] = [B[k][i] - q * B[j][i] for i in range(m)]
            B_star, mu = gram_schmidt(B)
            k += 1
    
    return B

def solve_subset_sum_lattice(pubkey, ciphertext):
    """Résout le problème subset-sum en utilisant LLL"""
    n = len(pubkey)
    
    # Construire la matrice du réseau
    # On utilise la matrice où chaque ligne i a 1 à la position i et pubkey[i] à la dernière position
    # Et la dernière ligne a 0 partout sauf -ciphertext à la dernière position
    
    # Matrice de taille (n+1) x (n+1)
    # Les n premières lignes: [e_i | pubkey[i]]
    # Dernière ligne: [0...0 | -ciphertext]
    
    size = n + 1
    M = [[0.0] * size for _ in range(size)]
    
    for i in range(n):
        M[i][i] = 1.0
        M[i][size-1] = float(pubkey[i])
    
    M[n][size-1] = -float(ciphertext)
    
    # Appliquer LLL
    reduced = lll(M)
    
    # Chercher un vecteur avec des entrées 0 ou 1
    for row in reduced:
        # Vérifier si c'est une solution valide
        vals = [round(x) for x in row[:-1]]
        if all(v in [0, 1] for v in vals):
            # Vérifier la somme
            total = sum(vals[i] * pubkey[i] for i in range(n))
            if total == ciphertext:
                return vals
    
    return None

# Testons avec le premier ciphertext
pubkey_str = """65363128684447571132776241699
11274630258057967396026665723
60559222278375482447330083794
70238185910865550789020602007
78077025115892356117353286514
68689714170530501420950259719
29127755965063579516555824180
32796713726379898017330479743
45519033311461958996652579847
59481922183281857526171199789
55495084400556906381284478613
14576717810183300603139843389
68589281729516899808716443746
20296909478473654757282621208
30537953005493837032599666770
50700906734420621772366528392
58720389817577647385263517768
14929982408329983159745130411
78957868028931941741179820628
31015553887459374066166570979
6479387240029285522500789709
44834052244814211323002768825
68880768174885210134417155701
70728065516536734229876378887
19940352925118383021332476475
11926610039430690869353776248
44284085306881906513505933290
65961141103798053905550707203
79222330366488147095589071397
57716218939764421264346243444
7143427741922311277425019977
40102124774314571307421209726
31106346336357167193152859646
9869211918329061407583377438
23696943552216795845779539234
57055944207555268510811881306
3327580670445191612826287616
10613681056449056256265359590
59950266048603035641387473838
58927069738258076769247034796
64441245461962817349401724273
49297856532179662020349932300
45182819049805987851607519281
35526859738167888566962688623
69627835129445026186765372626
42091939332905056814598857452
13191888117017754559626998031
45745228201887970683682373391
62110476246079115246893565460
34936923235681473070158040183
21488885432536346192206522870
71644808849324143031304224752
68376445195906361888347719926
51783851937617327120469134628
65557742112975106585661516908
54063485202872162576322297308
74075528359043450527980626626
42713815274261871699013795581
67529400689171140706681990106
21066253853172746373456494821
56109555611748530333568577993
18657428926348050402028051389
13281943995839590735434938781
41966820243972970004685470533
42715438945182202722984178323
58189724253003705746237182254
74448304789798298732507599455
10158206024125176882906547212
45737872490388506855671491388
52889203964129866973885109
50666903728700094028720106297
51522962071682837162170650478"""

ciphertext_str = """1599051655305089304826823929251
1797746206330633665893908016565
1661865493958450122592244546366
1514497994514640235239498547775
1612686994707484946937928105122
1910510829453185702573591325325
994664683904375893078154622717"""

pubkey = [int(x) for x in pubkey_str.strip().split('\n')]
ciphertexts = [int(x) for x in ciphertext_str.strip().split('\n')]

print("Test sur le premier ciphertext...")
result = solve_subset_sum_lattice(pubkey, ciphertexts[0])
if result:
    print("Solution trouvée!")
    print(f"Nombre de bits à 1: {sum(result)}")
else:
    print("Aucune solution trouvée avec LLL simple")