import base64

# La chaîne trouvée
encoded = b"Ml81dDNAMV8="
decoded = base64.b64decode(encoded)
print(f"Encoded: {encoded}")
print(f"Decoded: {decoded}")
print(f"Decoded as string: {decoded.decode('utf-8', errors='replace')}")

# Peut-être qu'il y a d'autres parties du flag cachées
# Cherchons des patterns qui pourraient être d'autres parties Base64
# ou des chaînes qui ressemblent à du flag

with open("12345678 (1).wav", "rb") as f:
    data = f.read()

# Chercher toutes les occurrences de "Ml81dDNAMV8="
import re
pattern = re.compile(rb'Ml81dDNAMV8=')
matches = list(pattern.finditer(data))
print(f"\nNombre d'occurrences de 'Ml81dDNAMV8=': {len(matches)}")
for m in matches:
    print(f"  Position: {m.start()}")

# Chercher des chaînes qui pourraient être le début ou la fin du flag
# Par exemple, chercher "csaw" ou "}"
if b"csaw" in data:
    idx = data.find(b"csaw")
    print(f"\n'csaw' trouvé à la position {idx}")
    print(f"Contexte: {data[idx:idx+20]}")

# Trouver toutes les occurrences de "}"
for i, b in enumerate(data):
    if b == ord('}'):
        print(f"'}' trouvé à la position {i}, contexte: " + str(data[max(0,i-10):i+10]))