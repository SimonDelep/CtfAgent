with open('session.bin', 'rb') as f:
    data = f.read()

# Affichons les octets autour de l'index 124
idx = 124
print("Octets autour de l'index 124:")
for i in range(idx, min(idx+100, len(data))):
    print(f"{i}: 0x{data[i]:02x} ({chr(data[i]) if 32 <= data[i] < 127 else '.'})")
