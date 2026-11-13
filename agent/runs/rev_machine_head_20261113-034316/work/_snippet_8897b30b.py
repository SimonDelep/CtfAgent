# Extraire les données après la chaîne "Correct! That's the master key."
with open('masterkey', 'rb') as f:
    data = f.read()

# Trouver la position de "Correct! That's the master key."
correct_str = b"Correct! That's the master key.\x00"
pos = data.find(correct_str)
print(f"Position de 'Correct!': {pos} (0x{pos:x})")

# Les données bytecode commencent après la chaîne
bytecode_start = pos + len(correct_str)
print(f"Bytecode commence à: {bytecode_start} (0x{bytecode_start:x})")

# Extraire le bytecode (jusqu'à la fin ou jusqu'à une limite raisonnable)
bytecode = data[bytecode_start:bytecode_start+500]
print(f"Bytecode (premier 200 octets):")
print(' '.join(f'{b:02x}' for b in bytecode[:200]))
print()
print("Bytecode en hex:")
for i in range(0, min(200, len(bytecode)), 16):
    hex_part = ' '.join(f'{b:02x}' for b in bytecode[i:i+16])
    ascii_part = ''.join(chr(b) if 32 <= b < 127 else '.' for b in bytecode[i:i+16])
    print(f"{bytecode_start+i:04x}: {hex_part:<48} {ascii_part}")