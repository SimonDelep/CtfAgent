ciphertext = "esnp{d0c_@yz@gl_mn0j_pm3z3_g0_o00s}"

# Si la clé est [6, 0, 15, 7] cyclique, on obtient csaw}d?dY...
# Mais si la clé est seulement [6, 0, 15, 7] pour les 4 premiers, puis 0 pour le reste ?

# Test: clé [6, 0, 15, 7] puis 0 pour le reste
def xor_decrypt_partial(ct, key_prefix, rest_key=0):
    result = []
    for i, c in enumerate(ct):
        if i < len(key_prefix):
            k = key_prefix[i]
        else:
            k = rest_key
        result.append(chr(ord(c) ^ k))
    return ''.join(result)

print("Clé [6,0,15,7] puis 0:")
print(xor_decrypt_partial(ciphertext, [6, 0, 15, 7], 0))

# Autre hypothèse: peut-être que le ciphertext est en fait le plaintext, et qu'il faut juste lire le message caché ?
# Ou peut-être que c'est un stéganographie dans la vidéo ?

# Vérifions d'abord le fichier vidéo
import subprocess
result = subprocess.run(['file', 'finderskeepers.mp4'], capture_output=True, text=True)
print(f"\nType de fichier: {result.stdout}")

# Regardons les premières octets
with open('finderskeepers.mp4', 'rb') as f:
    data = f.read(100)
    print(f"\nPremiers octets (hex): {data[:50].hex()}")
    print(f"Premiers octets (ascii): {data[:50]}")