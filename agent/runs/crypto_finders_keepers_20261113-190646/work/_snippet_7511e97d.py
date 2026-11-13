import base64

b64 = "ZXNucHtkMGNfQHl6QGdsX21uMGpfcG0zejNfZzBfbzAwc30="
decoded = base64.b64decode(b64).decode('utf-8')
print(f"Base64 décodé: {decoded}")