ciphertext = "esnp{d0c_@yz@gl_mn0j_pm3z3_g0_o00s}"

# Chiffrement de César : décalage constant
def caesar_decrypt(ciphertext, shift):
    result = []
    for c in ciphertext:
        if c.isalpha():
            if c.islower():
                result.append(chr((ord(c) - ord('a') - shift) % 26 + ord('a')))
            else:
                result.append(chr((ord(c) - ord('A') - shift) % 26 + 'A'))
        else:
            result.append(c)
    return ''.join(result)

# Essayer tous les décalages
for shift in range(26):
    result = caesar_decrypt(ciphertext, shift)
    if 'csaw' in result.lower() or 'you' in result.lower():
        print(f"Shift {shift}: {result}")

# Peut-être que le message est juste le ciphertext décodé sans Vigenère?
import base64
# Le ciphertext original est Base64 encodé
b64_ciphertext = "ZXNucHtkMGNfQHl6QGdsX21uMGpfcG0zejNfZzBfbzAwc30="
decoded = base64.b64decode(b64_ciphertext).decode('utf-8')
print(f"\nBase64 décodé: {decoded}")

# Peut-être que le message final est juste ce texte, sans Vigenère?
# Ou peut-être que c'est un autre type de transformation?
