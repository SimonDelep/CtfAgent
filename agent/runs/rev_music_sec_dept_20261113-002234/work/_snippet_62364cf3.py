import struct

with open('csirac/session.bin', 'rb') as f:
    data = f.read()

print(f"Taille: {len(data)} bytes")
print("Premiers 100 bytes (hex):")
print(data[:100].hex())
print()

# Chercher le pattern flag{
idx = data.find(b'flag{')
print(f"Index de 'flag{{': {idx}")

# Chercher le salt
salt_idx = data.find(b's4lt26')
print(f"Index de 's4lt26': {salt_idx}")

# Afficher les bytes autour de flag{
if idx >= 0:
    print(f"Bytes autour de flag{{: {data[idx:idx+20].hex()}")
    print(f"En clair: {data[idx:idx+20]}")

# Afficher les bytes autour du salt
if salt_idx >= 0:
    print(f"Bytes autour de s4lt26: {data[salt_idx:salt_idx+30].hex()}")