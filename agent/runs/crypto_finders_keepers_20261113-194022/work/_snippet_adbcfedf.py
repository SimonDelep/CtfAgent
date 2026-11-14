import base64

# La chaîne Base64 extraite précédemment
b64_str = "ZXNucHtkMGNfQHl6QGdsX21uMGpfcG0zejNfZzBfbzAwc30="
decoded = base64.b64decode(b64_str).decode('utf-8')
print(f"Base64 décodé: {decoded}")

# Texte déchiffré avec clé 'cantfind'
ciphertext = decoded  # 'esnp{d0c_@yz@gl_mn0j_pm3z3_g0_o00s}'

def vigenere_decrypt(ciphertext, key):
    result = []
    key_index = 0
    for char in ciphertext:
        if char.isalpha():
            # Déterminer si majuscule ou minuscule
            base = ord('A') if char.isupper() else ord('a')
            key_char = key[key_index % len(key)]
            key_shift = ord(key_char.lower()) - ord('a')
            decrypted_char = chr((ord(char) - base - key_shift) % 26 + base)
            result.append(decrypted_char)
            key_index += 1
        else:
            result.append(char)
    return ''.join(result)

# Tester avec la clé 'cantfind'
key = 'cantfind'
decrypted = vigenere_decrypt(ciphertext, key)
print(f"Déchiffré avec '{key}': {decrypted}")

# Tester avec d'autres clés possibles
keys_to_try = ['cant', 'find', 'cantfind', 'finders', 'keepers', 'cantfindme', 'cantfindit', 'finderskeepers']
for k in keys_to_try:
    d = vigenere_decrypt(ciphertext, k)
    print(f"Clé '{k}': {d}")