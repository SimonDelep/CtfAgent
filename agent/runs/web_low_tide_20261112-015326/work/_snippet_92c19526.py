import base64

# La chaîne encodée depuis app.js
encoded = "4@?DE vp%t(p*      b5 a_ aa e` cg da b_ eb cc e7 fe c4 ba fg fe ec fh b` b_ e` df da e4 c4 df fg eh c4 e5 c6 b_ d2 eh bd e2 eb ba ce bb c4 e5 e4 fe c7 e2 ef ff c7 cc c` fe eb bb da eg ec cf e4 fe ea eh bh e2 e` cf de e2 e` ba e4 fd aa b3"

# Étape 1: rot47
def rot47(s):
    result = []
    for c in s:
        code = ord(c)
        if 33 <= code <= 126:
            code = 33 + ((code - 33 + 47) % 94)
        result.append(chr(code))
    return ''.join(result)

rot47_once = rot47(encoded)
print("Après rot47:")
print(rot47_once)

# Extraire la partie hexadécimale (après "const GATEWAY")
# La chaîne contient "const GATEWAY" suivi de la vraie valeur
# Je vais chercher la partie qui ressemble à du hex (paires de caractères hex)
import re

# Trouver toutes les paires hex (caractères hexadécimaux)
hex_pairs = re.findall(r'[0-9a-f]{2}', rot47_once.lower())
print("\nPaires hex trouvées:")
print(''.join(hex_pairs))

hex_str = ''.join(hex_pairs)
print(f"\nLongueur: {len(hex_str)}")

try:
    decoded_bytes = bytes.fromhex(hex_str)
    print("\nDécodage hex réussi:")
    print(decoded_bytes)
    
    decoded_base64 = decoded_bytes.decode('ascii', errors='ignore')
    print("\nBase64 string:")
    print(decoded_base64)
    
    final = base64.b64decode(decoded_base64).decode('utf-8')
    print("\nDécodage final (base64):")
    print(final)
except Exception as e:
    print(f"Erreur: {e}")