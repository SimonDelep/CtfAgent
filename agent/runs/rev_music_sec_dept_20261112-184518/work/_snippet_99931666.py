with open('session.bin', 'rb') as f:
    data = f.read()

# Chercher le pattern 0x81 + 'f' (0x66) = 0xe7
# 'flag{' en encodage 0x81+ASCII serait: 0xe7 0xe8 0xe9 0xea 0xe1
pattern = bytes([0x81 + ord(c) for c in 'flag{'])
print(f"Pattern recherché (flag{{ en 0x81+ASCII): {pattern.hex()}")

idx = data.find(pattern)
print(f"Offset de 'flag' encodé: {idx}")

if idx >= 0:
    # Extraire les 5 octets
    print(f"Données à cet offset: {data[idx:idx+5].hex()}")
    # Décode
    decoded = ''.join(chr(b - 0x81) for b in data[idx:idx+5])
    print(f"Décodé: {decoded}")
    
    # Regardons plus loin - peut-être que le flag est chiffré après
    print(f"\nDonnées brutes autour: {data[idx:idx+30].hex()}")
else:
    # Cherchons autre chose
    print("Pattern non trouvé, cherchons autre chose...")
    # Peut-être que c'est juste 0x81 suivi du caractère
    for i in range(len(data)-4):
        if data[i] == 0x81:
            # Vérifier si c'est 'f'
            if data[i+1] == 0x81 + ord('f'):
                print(f"Trouvé à {i}")
                break
