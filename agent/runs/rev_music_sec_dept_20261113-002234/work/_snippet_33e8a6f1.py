with open('csirac/session.bin', 'rb') as f:
    data = f.read()

# Chercher le pattern 0x81 XX qui semble être un encodage
print("Recherche du pattern 0x81:")
for i, b in enumerate(data):
    if b == 0x81:
        print(f"  Offset {i}: 0x81 0x{data[i+1]:02x} = '{chr(data[i+1]) if 32 <= data[i+1] < 127 else '?'}'")

# Chercher le pattern flag{ encodé (0x81 0x66 pour 'f', etc.)
# 'f' = 0x66, 'l' = 0x6c, 'a' = 0x61, 'g' = 0x67, '{' = 0x7b
print("\nRecherche de 'flag{' encodé (0x81 0x66 0x81 0x6c ...):")
pattern = bytes([0x81, 0x66, 0x81, 0x6c, 0x81, 0x61, 0x81, 0x67, 0x81, 0x7b])
idx = data.find(pattern)
print(f"Index: {idx}")
if idx >= 0:
    print(f"Bytes: {data[idx:idx+20].hex()}")