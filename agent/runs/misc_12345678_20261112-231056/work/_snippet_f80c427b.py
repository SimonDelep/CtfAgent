import struct

# Lire le fichier WAV
with open('audio.wav', 'rb') as f:
    data = f.read()

# Trouver le chunk 'data'
data_start = data.find(b'data')
if data_start != -1:
    data_start += 8
    audio_data = data[data_start:]
    
    # Extraire tous les échantillons
    samples = []
    for i in range(0, len(audio_data), 2):
        if i + 2 <= len(audio_data):
            val = struct.unpack('<h', audio_data[i:i+2])[0]
            samples.append(val)
    
    # Extraire LSB
    lsb_bits = [s & 1 for s in samples]
    
    # Convertir en bytes (little-endian bit order)
    bytes_from_lsb = []
    for i in range(0, len(lsb_bits) - 7, 8):
        byte_val = 0
        for j in range(8):
            byte_val |= (lsb_bits[i + j] << j)
        bytes_from_lsb.append(byte_val)
    
    # Chercher 'csaw{' ou '{'
    result = bytes(bytes_from_lsb)
    
    # Chercher la séquence 'csaw{'
    target = b'csaw{'
    idx = result.find(target)
    if idx != -1:
        print(f"Trouvé 'csaw{' à l'index {idx}")
        print("Contexte:", result[idx:idx+100])
    else:
        # Chercher juste '{'
        idx = result.find(b'{')
        if idx != -1:
            print(f"Trouvé '{{' à l'index {idx}")
            print("Contexte:", result[max(0, idx-10):idx+100])
    
    # Afficher plus de données brutes autour du début
    print("\nPremiers 500 bytes:")
    print(result[:500])