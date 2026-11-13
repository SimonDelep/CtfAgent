# Peut-être que le contenu entre accolades est chiffré avec une clé différente ?
# Le message chiffré est "esnp{d0c_@yz@gl_mn0j_pm3z3_g0_o00s}"
# Le contenu entre accolades est "d0c_@yz@gl_mn0j_pm3z3_g0_o00s"

# Essayons de trouver une clé qui transforme ce contenu en un message lisible
# Peut-être que la clé est "csaw" ou quelque chose comme ça ?

content = "d0c_@yz@gl_mn0j_pm3z3_g0_o00s"

# Essayons de XOR avec différentes clés
for key_len in range(1, 10):
    for key_start in range(256):
        # Clé cyclique de longueur key_len, commençant à key_start
        key = [(key_start + i) % 256 for i in range(key_len)]
        result = []
        for i, c in enumerate(content):
            k = key[i % len(key)]
            result.append(chr(ord(c) ^ k))
        result_str = ''.join(result)
        # Vérifions si le résultat contient des lettres minuscules ou des underscores
        if result_str.isalnum() or '_' in result_str or result_str.replace('_', '').isalnum():
            # Vérifions si le résultat ressemble à un message lisible
            if result_str.islower() or result_str.replace('_', '').islower():
                print(f"Clé {key}: {result_str}")

# Trop de résultats... essayons une approche différente
# Peut-être que le contenu est chiffré avec la clé [6, 0, 15, 7] mais en commençant à une position différente ?

key = [6, 0, 15, 7]
for start in range(4):
    result = []
    for i, c in enumerate(content):
        k = key[(i + start) % 4]
        result.append(chr(ord(c) ^ k))
    print(f"Start {start}: {''.join(result)}")