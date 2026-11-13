# Analyser la structure complète de session.bin
with open('csirac/session.bin', 'rb') as f:
    data = f.read()

# Chercher toutes les occurrences de 0x81
positions_81 = [i for i, b in enumerate(data) if b == 0x81]
print("Positions de 0x81:", positions_81[:30])

# Chercher "csaw" ou "csaw{"
for pattern in [b'csaw', b'csaw{', b'csaw}', b'FLAG', b'FLAG{']:
    pos = data.find(pattern)
    if pos != -1:
        print(f"Trouve '{pattern}' a la position {pos}")

# Chercher "}" (0x7d)
close_brace = data.find(0x7d)
print("Position de 0x7d (}):", close_brace)

# Chercher 0x81 0x7d (}" encodé)
close_brace_enc = data.find(bytes([0x81, 0x7d]))
print("Position de 0x81 0x7d (}} encodé):", close_brace_enc)

# Regardons le contenu autour de "flag{"
print("\n--- Contenu autour de flag{ (positions 120-200) ---")
print(data[120:200].hex())
print(data[120:200])