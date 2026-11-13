# Analyser la structure après "flag{"
with open('session.bin', 'rb') as f:
    data = f.read()

# Trouver "flag{"
flag_start = None
for i in range(len(data)-8):
    if data[i:i+10] == bytes([0x81, 0x66, 0x81, 0x6c, 0x81, 0x61, 0x81, 0x67, 0x81, 0x7b]):
        flag_start = i
        break

if flag_start:
    # Après "flag{" (10 octets), on a:
    # 0x81 0x0a = newline
    # 02 00 00 00 = peut-être une longueur (2?) ou un type
    # Puis des données
    
    print("Structure après 'flag{':")
    print(f"  0x81 0x0a = newline")
    print(f"  Bytes suivants: {data[flag_start+10:flag_start+14].hex()}")
    
    # Après les 4 bytes, il y a des données
    data_start = flag_start + 14
    print(f"\nDonnées à partir de {data_start}:")
    print(data[data_start:data_start+100].hex())
    
    # Chercher la fin du flag - peut-être qu'il y a un marqueur de fin
    # Regardons si on trouve "}" ou un marqueur spécial
    
    # Chercher "}" encodé (0x81 0x7d)
    for i in range(data_start, min(data_start+500, len(data)-1)):
        if data[i] == 0x81 and i+1 < len(data) and data[i+1] == 0x7d:
            print(f"\nTrouvé '}}' à la position {i}")
            break
    
    # Chercher aussi "}" non encodé
    for i in range(data_start, min(data_start+500, len(data))):
        if data[i] == 0x7d:
            print(f"Trouvé '}}' (non encodé) à la position {i}")
            break