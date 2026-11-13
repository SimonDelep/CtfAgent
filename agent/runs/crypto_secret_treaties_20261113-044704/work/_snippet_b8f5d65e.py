# Essayons de résoudre le premier ciphertext avec une approche plus intelligente
# On va utiliser une approche de recherche avec élagage, mais en optimisant

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

pubkey = [int(x) for x in pubkey_str.strip().split('\n')]
ciphertext = 1599051655305089304826823929251

# Le problème est que 2^72 est trop grand pour une recherche exhaustive
# Mais peut-être que le nombre de bits à 1 est petit?

# Calculons le nombre moyen de bits à 1 attendu
# Si le message est du texte ASCII, chaque byte a environ 4-5 bits à 1 en moyenne
# Donc 9 bytes * 4.5 = ~40 bits à 1 en moyenne

# Essayons une approche différente: utiliser LLL en pur Python
# On va implémenter LLL simplifié

def lll_reduce(matrix, delta=0.75):
    """
    Implémentation simplifiée de LLL en pur Python
    """
    n = len(matrix)
    m = len(matrix[0])
    
    # Convertir en nombres rationnels pour éviter les erreurs d'arrondi
    from fractions import Fraction
    
    # Créer une matrice de Fractions
    M = [[Fraction(matrix[i][j]) for j in range(m)] for i in range(n)]
    
    # Gram-Schmidt
    def gram_schmidt(M):
        n = len(M)
        m = len(M[0])
        Q = [[Fraction(0) for _ in range(m)] for _ in range(n)]
        mu = [[Fraction(0) for _ in range(n)] for _ in range(n)]
        norm_sq = [Fraction(0) for _ in range(n)]
        
        for i in range(n):
            for j in range(m):
                Q[i][j] = M[i][j]
            for k in range(i):
                # mu[i][k] = <M[i], Q[k]> / <Q[k], Q[k]>
                dot_mk = sum(M[i][j] * Q[k][j] for j in range(m))
                dot_kk = sum(Q[k][j] * Q[k][j] for j in range(m))
                if dot_kk != 0:
                    mu[i][k] = dot_mk / dot_kk
                    for j in range(m):
                        Q[i][j] -= mu[i][k] * Q[k][j]
            norm_sq[i] = sum(Q[i][j] * Q[i][j] for j in range(m))
        
        return Q, mu, norm_sq
    
    # LLL reduction
    k = 0
    while k < n - 1:
        Q, mu, norm_sq = gram_schmidt(M)
        
        # Condition de Lovasz
        if norm_sq[k] == 0:
            k += 1
            continue
            
        if delta * norm_sq[k] <= norm_sq[k+1] + mu[k+1][k] * mu[k+1][k] * norm_sq[k]:
            k += 1
        else:
            # Échange
            M[k], M[k+1] = M[k+1], M[k]
            k = max(k - 1, 0)
    
    # Réduction
    for i in range(n):
        for j in range(i-1, -1, -1):
            Q, mu, norm_sq = gram_schmidt(M)
            r = round(mu[i][j])
            if r != 0:
                for col in range(m):
                    M[i][col] -= r * M[j][col]
    
    return [[int(M[i][j]) for j in range(m)] for i in range(n)]

# Construire la matrice pour LLL
# On cherche x ∈ {0,1}^n tel que sum(pubkey[i] * x[i]) = target
# La matrice est de la forme:
# [ I_n    0 ]
# [ a^T   -c ]
# où a est le vecteur pubkey et c est le target

n = len(pubkey)
target = ciphertext

# Construire la matrice
matrix = [[0] * (n + 1) for _ in range(n + 1)]

# Les n premières lignes: identité
for i in range(n):
    matrix[i][i] = 1

# Dernière ligne: pubkey et -target
for i in range(n):
    matrix[n][i] = pubkey[i]
matrix[n][n] = -target

print(f"Matrice de dimension {n+1}x{n+1}")
print(f"Première ligne: {matrix[0][:5]}...")
print(f"Dernière ligne: {matrix[n][:5]}... {matrix[n][n]}")

# Appliquer LLL
print("Appliquons LLL...")
import time
start = time.time()
reduced = lll_reduce(matrix)
end = time.time()
print(f"LLL terminé en {end - start:.2f}s")

# Chercher un vecteur court qui correspond à la solution
# Le vecteur solution devrait avoir une norme petite
print("\nRecherche de vecteur solution...")
for i in range(n + 1):
    norm = sum(x*x for x in reduced[i])
    if norm < 100:  # Vecteur court
        print(f"Ligne {i}: norme = {norm}, vecteur = {reduced[i][:10]}...")