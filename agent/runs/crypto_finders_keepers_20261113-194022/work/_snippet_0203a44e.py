import base64

# Première chaîne
b64_1 = "W5M0MpCehiHzreSzNTczkc9d"
try:
    decoded_1 = base64.b64decode(b64_1).decode('utf-8', errors='replace')
    print(f"Chaîne 1: {b64_1}")
    print(f"Décodé: {decoded_1}")
except Exception as e:
    print(f"Erreur décodage chaîne 1: {e}")

# Deuxième chaîne (celle qu'on a déjà décodée)
b64_2 = "ZXNucHtkMGNfQHl6QGdsX21uMGpfcG0zejNfZzBfbzAwc30="
try:
    decoded_2 = base64.b64decode(b64_2).decode('utf-8')
    print(f"\nChaîne 2: {b64_2}")
    print(f"Décodé: {decoded_2}")
except Exception as e:
    print(f"Erreur décodage chaîne 2: {e}")