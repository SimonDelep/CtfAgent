# Approche alternative: chercher m en utilisant le fait que
# pour une séquence super-croissante, les éléments croissent rapidement
# et m doit être > sum(a)

# Une autre approche: utiliser le fait que si on multiplie tous les b[i] par w^{-1} mod m,
# on obtient une séquence super-croissante

# Essayons de trouver m en cherchant un nombre tel que quand on divise les b[i] par m,
# on obtient des restes qui forment une séquence super-croissante

# D'abord, calculons la somme de la clé publique
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

total_sum = sum(pubkey)
print(f"Somme totale de la clé publique: {total_sum}")
print(f"Nombre d'éléments: {len(pubkey)}")

# Pour Merkle-Hellman, m > sum(a) où a est la séquence super-croissante
# Mais b[i] = (a[i] * w) mod m, donc b[i] < m
# Le plus grand b[i] doit être < m

max_b = max(pubkey)
print(f"Max de la clé publique: {max_b}")

# m doit être > max(pubkey) et probablement > sum(a)
# Une estimation: m est probablement autour de 2 * sum(a) ou plus

# Essayons une approche différente: utiliser le GCD
# Si on prend deux éléments b[i] et b[j], leur GCD peut révéler des informations sur m

import math
gcd_all = pubkey[0]
for b in pubkey[1:]:
    gcd_all = math.gcd(gcd_all, b)
    if gcd_all == 1:
        break
print(f"GCD de tous les éléments: {gcd_all}")

# Si le GCD est 1, on peut essayer de trouver m en cherchant un nombre tel que
# quand on calcule (b[i] * w^{-1}) mod m, on obtient une séquence super-croissante

# Une autre idée: pour Merkle-Hellman, souvent m est un nombre premier ou proche d'une puissance de 2
# Essayons de voir si m pourrait être lié à la somme totale

# La somme totale est environ 3.18e30
# m doit être > sum(a), et sum(a) < sum(b) si w < m

# Essayons de trouver m en cherchant autour de la somme totale
print(f"\nRecherche de m autour de la somme totale...")
print(f"Somme totale: {total_sum}")

# Une approche: si on suppose que w est petit, alors b[i] ≈ a[i] * w
# Donc a[i] ≈ b[i] / w
# Et sum(a) ≈ sum(b) / w

# Pour une séquence super-croissante de 72 éléments, sum(a) est dominé par le dernier élément
# Le dernier élément a[71] > sum(a[0..70])

# Essayons une approche par recherche de m
# On sait que m > sum(a) et b[i] = (a[i] * w) mod m

# Si on prend le plus grand élément de b, disons b_max, alors b_max < m
# Et m doit être tel que quand on multiplie par w^{-1} mod m, on obtient une séquence super-croissante

# Essayons de trouver m en testant des valeurs autour de la somme totale
# Mais d'abord, vérifions si m pourrait être un nombre premier proche de la somme

def is_prime(n):
    if n < 2:
        return False
    if n == 2:
        return True
    if n % 2 == 0:
        return False
    for i in range(3, int(n**0.5) + 1, 2):
        if n % i == 0:
            return False
    return True

# La somme est trop grande pour tester tous les nombres
# Essayons une approche différente: utiliser le fait que pour une séquence super-croissante,
# les éléments croissent au moins de factor 2

# Une autre approche: utiliser LLL pour trouver la trapdoor directement
# Construire une matrice où le vecteur court correspond à (w, m)

print("\nApproche LLL pour trouver la trapdoor...")
print("On cherche w et m tels que b[i] = (a[i] * w) mod m avec a super-croissante")