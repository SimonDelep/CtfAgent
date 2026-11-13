# Implémentation LLL optimisée avec entiers
import math
import time

def lll_int(B, delta=3, threshold=3):
    """LLL avec entiers (delta = delta * 4 pour éviter les floats)"""
    n = len(B)
    m = len(B[0])
    
    # Convertir en entiers (multiplier par une grande puissance de 2 pour la précision)
    scale = 2**60
    B = [[int(x * scale) for x in row] for row in B]
    
    # Gram-Schmidt avec entiers
    def gs(B):
        n = len(B)
        m = len(B[0])
        B_star = [[B[i][j] for j in range(m)] for i in range(n)]
        mu_num = [[0] * n for _ in range(n)]  # numérateur de mu
        mu_den = [1] * n  # dénominateur (norme au carré)
        
        for i in range(n):
            for j in range(i):
                # mu[i][j] = dot(B_star[i], B_star[j]) / dot(B_star[j], B_star[j])
                dot = sum(B_star[i][k] * B_star[j][k] for k in range(m))
                norm_j = sum(B_star[j][k] ** 2 for k in range(m))
                if norm_j != 0:
                    mu_num[i][j] = dot
                    mu_den[i] = norm_j
                    # B_star[i] -= mu[i][j] * B_star[j]
                    for k in range(m):
                        B_star[i][k] = B_star[i][k] * mu_den[i] - mu_num[i][j] * B_star[j][k]
                    # Normaliser B_star[i]
                    for k in range(m):
                        B_star[i][k] //= mu_den[i]
        
        return B_star, mu_num, mu_den
    
    B_star, mu_num, mu_den = gs(B)
    
    k = 1
    max_iter = n * 100
    iter_count = 0
    
    while k < n and iter_count < max_iter:
        iter_count += 1
        
        # Condition de Lovasz: delta * ||b*_k-1||^2 <= ||b*_k||^2
        norm_km1 = sum(B_star[k-1][j] ** 2 for j in range(m))
        norm_k = sum(B_star[k][j] ** 2 for j in range(m))
        
        if delta * norm_km1 > norm_k:
            # Échange
            B[k-1], B[k] = B[k], B[k-1]
            B_star, mu_num, mu_den = gs(B)
            k = max(1, k - 1)
        else:
            # Condition de taille: |mu[k][j]| <= 1/2
            for j in range(k):
                if mu_den[j] != 0:
                    mu_val = mu_num[k][j] / mu_den[j]
                    if abs(mu_val) > 0.5:
                        q = round(mu_val)
                        for i in range(m):
                            B[k][i] -= q * B[j][i]
            B_star, mu_num, mu_den = gs(B)
            k += 1
    
    # Convertir de retour
    B = [[x // scale for x in row] for row in B]
    return B

def solve_subset_sum_lattice(pubkey, ciphertext):
    n = len(pubkey)
    
    # Construire la matrice (n+1) x (n+1)
    # Lignes 0..n-1: e_i avec pubkey[i] à la dernière colonne
    # Ligne n: [0...0 | -ciphertext]
    
    size = n + 1
    M = [[0] * size for _ in range(size)]
    
    for i in range(n):
        M[i][i] = 1
        M[i][size-1] = pubkey[i]
    
    M[n][size-1] = -ciphertext
    
    # LLL
    reduced = lll_int(M)
    
    # Chercher un vecteur avec entrées 0 ou 1
    for row in reduced:
        vals = [row[i] for i in range(n)]
        if all(v in [0, 1] for v in vals):
            total = sum(vals[i] * pubkey[i] for i in range(n))
            if total == ciphertext:
                return vals
    
    return None

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

start = time.time()
print("Test sur le premier ciphertext...")
result = solve_subset_sum_lattice(pubkey, ciphertexts[0])
elapsed = time.time() - start
print(f"Temps: {elapsed:.2f}s")
if result:
    print("Solution trouvée!")
    print(f"Nombre de bits à 1: {sum(result)}")
else:
    print("Aucune solution trouvée")