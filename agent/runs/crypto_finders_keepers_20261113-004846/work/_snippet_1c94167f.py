import base64

encoded = "ZXNucHtkMGNfQHl6QGdsX21uMGpfcG0zejNfZzBfbzAwc30="
decoded = base64.b64decode(encoded).decode('utf-8')
print("Décodage Base64:", decoded)

# C'est "esnph{d0c_@yz@gl_mn0j_pm3z3_g0_o00s}"
# Le préfixe est "esnph{" au lieu de "csaw{"
# Vérifions la différence XOR
prefix_encoded = "esnph"
prefix_expected = "csaw{"

for i, (a, b) in enumerate(zip(prefix_encoded, prefix_expected)):
    xor_val = ord(a) ^ ord(b)
    print(f"Position {i}: '{a}' ^ '{b}' = {xor_val} (0x{xor_val:02x})")