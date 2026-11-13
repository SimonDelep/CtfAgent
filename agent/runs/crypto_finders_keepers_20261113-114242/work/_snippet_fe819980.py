# Si on connaît le plain attendu "csaw{...}" et le cipher "esnp{...}"
# On peut trouver la clé

cipher = "esnp"
plain_expected = "csaw"

def find_key(cipher, plain):
    key = []
    for c, p in zip(cipher, plain):
        c_val = ord(c.lower()) - ord('a')
        p_val = ord(p.lower()) - ord('a')
        # cipher = (plain + key) mod 26
        # key = (cipher - plain) mod 26
        k_val = (c_val - p_val) % 26
        key.append(chr(k_val + ord('a')))
    return ''.join(key)

print("Clé pour esnp->csaw:", find_key(cipher, plain_expected))

# Maintenant appliquons cette clé au reste du message
# La clé semble être "uc" ou quelque chose comme ça

# Vérifions: e(4) - c(2) = 2 = c, s(18) - a(0) = 18 = s, n(13) - s(18) = -5 = v, p(15) - w(22) = -7 = t
# Donc la clé serait "csvt" ?

# Recalculons
cipher = "esnp"
plain_expected = "csaw"
for i, (c, p) in enumerate(zip(cipher, plain_expected)):
    c_val = ord(c.lower()) - ord('a')
    p_val = ord(p.lower()) - ord('a')
    k_val = (c_val - p_val) % 26
    print(f"{c} -> {p}: key = {k_val} = '{chr(k_val + ord('a'))}'")