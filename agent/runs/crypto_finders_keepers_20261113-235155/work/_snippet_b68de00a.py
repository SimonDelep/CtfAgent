import base64

ciphertext_b64 = "ZXNucHtkMGNfQHl6QGdsX21uMGpfcG0zejNfZzBfbzAwc30="
ciphertext = base64.b64decode(ciphertext_b64).decode('latin-1')
print(f"Ciphertext: {ciphertext}")
print(f"Length: {len(ciphertext)}")