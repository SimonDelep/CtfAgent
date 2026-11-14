with open('masterkey', 'rb') as f:
    data = f.read()

rodata_offset = 0x2000
rodata_data = data[rodata_offset:rodata_offset+0x8a0]

# Chercher "Correct"
correct_pos = rodata_data.find(b'Correct')
print(f"Position de 'Correct': {hex(correct_pos)}")

# Chercher "Wrong"
wrong_pos = rodata_data.find(b'Wrong')
print(f"Position de 'Wrong': {hex(wrong_pos)}")

# Afficher autour de "Correct"
if correct_pos >= 0:
    start = max(0, correct_pos - 16)
    end = min(len(rodata_data), correct_pos + 64)
    print(f"\nDonnées autour de 'Correct' ({hex(correct_pos)}):")
    for i in range(start, end, 16):
        hex_str = ' '.join(f'{b:02x}' for b in rodata_data[i:i+16])
        ascii_str = ''.join(chr(b) if 32 <= b < 127 else '.' for b in rodata_data[i:i+16])
        print(f"{0x2000+i:04x}: {hex_str:<48} {ascii_str}")