# Lisons les premiers octets du fichier pour voir la structure
with open('finderskeepers.mp4', 'rb') as f:
    data = f.read(1000)
    print("Premiers 1000 octets (hex):")
    print(data[:200].hex())
    print("\nReprésentation ASCII:")
    for i in range(0, min(200, len(data)), 16):
        hex_part = ' '.join(f'{b:02x}' for b in data[i:i+16])
        ascii_part = ''.join(chr(b) if 32 <= b < 127 else '.' for b in data[i:i+16])
        print(f"{i:04x}: {hex_part:<48} {ascii_part}")