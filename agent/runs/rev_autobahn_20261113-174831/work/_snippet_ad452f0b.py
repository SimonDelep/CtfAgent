# Analyser la section .text avant enccode pour trouver la routine de déchiffrement
with open('nitro', 'rb') as f:
    data = f.read()

# .text: adresse 0x4010f0, offset 0x10f0
# enccode: adresse 0x40130d, offset 0x130d
# Donc .text va de 0x10f0 à 0x130d (environ 541 octets)

text_offset = 0x10f0
text_end = 0x130d
text_data = data[text_offset:text_end]

print(f"=== Section .text (offset 0x{text_offset:x} à 0x{text_end:x}, taille {len(text_data)}) ===")

# Afficher en hex avec décalage
for i in range(0, len(text_data), 32):
    hex_part = ' '.join(f'{b:02x}' for b in text_data[i:i+32])
    ascii_part = ''.join(chr(b) if 32 <= b < 127 else '.' for b in text_data[i:i+32])
    print(f"{text_offset + i:08x}: {hex_part:<96} {ascii_part}")

# Chercher des motifs intéressants comme "baad" ou "f00d"
print("\n=== Recherche de motifs ===")
for pattern in [b'\xba\xad', b'\xf0\x0d', b'baad', b'f00d']:
    idx = text_data.find(pattern)
    if idx != -1:
        print(f"Motif {pattern!r} trouvé à offset relatif {idx} (absolu {text_offset + idx})")