with open('session.bin', 'rb') as f:
    data = f.read()

print(f"Taille du fichier: {len(data)}")

# Afficher tout le fichier en hex par blocs de 32
for i in range(0, len(data), 32):
    chunk = data[i:i+32]
    hex_str = ' '.join(f'{b:02x}' for b in chunk)
    # Afficher aussi le texte ASCII si possible
    ascii_str = ''.join(chr(b) if 32 <= b < 127 else '.' for b in chunk)
    print(f"{i:04x}: {hex_str:<96} {ascii_str}")
