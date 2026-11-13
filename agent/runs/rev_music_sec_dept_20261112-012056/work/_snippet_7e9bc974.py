# Lire le fichier binaire
with open('csirac/session.bin', 'rb') as f:
    data = f.read()

# Chercher la séquence 81 66 81 6c 81 61 81 67 81 7b (flag{ avec préfixe 0x81)
flag_pattern = bytes([0x81, 0x66, 0x81, 0x6c, 0x81, 0x61, 0x81, 0x67, 0x81, 0x7b])
flag_start = data.find(flag_pattern)

print("Autour de flag{ (offset", flag_start, "):")
for i in range(max(0, flag_start-10), min(len(data), flag_start+60)):
    print(f"{i:3d}: 0x{data[i]:02x} ({chr(data[i]) if 32 <= data[i] < 127 else '.'})")
