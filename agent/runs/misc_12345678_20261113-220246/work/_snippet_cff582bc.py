# Trouver et analyser le chunk ID3
with open('audio.wav', 'rb') as f:
    data = f.read()

# Chercher ID3
idx = data.find(b'ID3 ')
if idx >= 0:
    print(f"ID3 trouvé à la position {idx}")
    # Le chunk ID3 commence par "ID3 " suivi de la taille
    chunk_size = int.from_bytes(data[idx+4:idx+8], 'little')
    print(f"Taille du chunk ID3: {chunk_size}")
    
    id3_data = data[idx:idx+8+chunk_size]
    print(f"Contenu ID3 (brut): {id3_data[:100]}")
    
    # Chercher des strings dans ID3
    import re
    strings = re.findall(rb'[\x20-\x7e]{4,}', id3_data)
    print(f"\nStrings trouvées dans ID3:")
    for s in strings:
        print(f"  {s}")
else:
    print("ID3 non trouvé")

# Chercher aussi "TXXX" ou autres frames ID3
if idx >= 0:
    # Les frames ID3 commencent après l'en-tête de 10 octets
    # En-tête ID3: ID3<version><flags><size>
    print(f"\nAnalyse détaillée de l'en-tête ID3:")
    print(f"  Signature: {id3_data[0:3]}")
    print(f"  Version: {id3_data[3:5]}")
    print(f"  Flags: {id3_data[5]}")
    size_bytes = id3_data[6:10]
    # Taille ID3 est encodée en synchsafe integer
    size = (size_bytes[0] << 21) | (size_bytes[1] << 14) | (size_bytes[2] << 7) | size_bytes[3]
    print(f"  Taille (synchsafe): {size}")