with open('session.bin', 'rb') as f:
    data = f.read()

# Affichons les bytes autour de 0x7c
print("Bytes de 0x7c à 0x90:")
for i in range(0x7c, min(0x90, len(data))):
    print(f"{i:04x}: {data[i]:02x} ({chr(data[i]) if 32 <= data[i] < 127 else '.'})")