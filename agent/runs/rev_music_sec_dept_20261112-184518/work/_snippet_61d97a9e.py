with open('session.bin', 'rb') as f:
    data = f.read()

# Cherchons le pattern exact de 'flag{' encodé
# 'f' = 0x66, donc 0x81 + 0x66 = 0xe7
# 'l' = 0x6c, donc 0x81 + 0x6c = 0xed
# 'a' = 0x61, donc 0x81 + 0x61 = 0xe2
# 'g' = 0x67, donc 0x81 + 0x67 = 0xe8
# '{' = 0x7b, donc 0x81 + 0x7b = 0xfc

pattern = bytes([0xe7, 0xed, 0xe2, 0xe8, 0xfc])
print(f"Pattern recherché: {pattern.hex()}")

idx = data.find(pattern)
print(f"Offset trouvé: {idx} (0x{idx:x})")

if idx >= 0:
    # Extraire et décoder
    encoded = data[idx:idx+5]
    print(f"Bytes encodés: {encoded.hex()}")
    decoded = ''.join(chr(b - 0x81) for b in encoded)
    print(f"Décodé: {decoded}")
    
    # Regardons ce qui suit
    print(f"\nDonnées après 'flag{{':")
    print(' '.join(f'{b:02x}' for b in data[idx+5:idx+30]))
else:
    # Cherchons manuellement
    print("Pattern non trouvé, cherchons 0x81 suivi de caractères...")
    for i in range(len(data)-4):
        if data[i] == 0x81:
            # Vérifier si c'est le début de 'flag{'
            if i+4 < len(data):
                # Vérifier le pattern
                chunk = data[i:i+5]
                if all(b >= 0x81 for b in chunk):
                    # C'est potentiellement du texte encodé
                    try:
                        decoded = ''.join(chr(b - 0x81) for b in chunk)
                        if 'flag' in decoded.lower() or decoded.startswith('flag'):
                            print(f"Trouvé à {i}: {chunk.hex()} -> {decoded}")
                    except:
                        pass
