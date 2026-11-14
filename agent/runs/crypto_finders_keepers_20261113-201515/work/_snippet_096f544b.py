# Peut-être que 'jc' signifie quelque chose comme 'jeu de caractères' ou un décalage spécifique
# 'j' = 9, 'c' = 2 en 0-indexed (a=0, b=1, c=2, ..., j=9)

ciphertext = "esnp{d0c_@yz@gl_mn0j_pm3z3_g0_o00s}"

# Essayons un décalage basé sur 'jc' = (9, 2) ou quelque chose comme ça
# Ou peut-être que 'jc' est une clé Vigenère courte

def vigenere_decrypt(ciphertext, key):
    result = []
    key_idx = 0
    for c in ciphertext:
        if c.isalpha():
            shift = ord(key[key_idx % len(key)].lower()) - ord('a')
            if c.islower():
                result.append(chr((ord(c) - ord('a') - shift) % 26 + ord('a')))
            else:
                result.append(chr((ord(c) - ord('A') - shift) % 26 + ord('A')))
            key_idx += 1
        else:
            result.append(c)
    return ''.join(result)

# Essayons toutes les clés de longueur 2
import string
letters = string.ascii_lowercase

# Peut-être que 'jc' est la clé, mais appliquée différemment
# Ou peut-être que c'est une clé différente

# Essayons de brute-force les clés de longueur 2
best_results = []
for k1 in letters:
    for k2 in letters:
        key = k1 + k2
        result = vigenere_decrypt(ciphertext, key)
        # Vérifier si le résultat commence par 'csaw{'
        if result.startswith('csaw{'):
            best_results.append((key, result))

print("Clés de longueur 2 donnant 'csaw{':")
for key, result in best_results[:20]:
    print(f"  {key}: {result}")
