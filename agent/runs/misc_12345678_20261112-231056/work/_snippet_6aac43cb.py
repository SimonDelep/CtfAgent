import wave

# Ouvrir le fichier WAV
with wave.open('audio.wav', 'rb') as wf:
    data = wf.readframes(wf.getnframes())
    sampwidth = wf.getsampwidth()
    
    # Extraire tous les échantillons
    samples = []
    for i in range(0, len(data), sampwidth):
        sample = int.from_bytes(data[i:i+sampwidth], byteorder='little', signed=True)
        samples.append(sample)
    
    # Extraire LSB
    lsb_bits = [s & 1 for s in samples]
    
    # Convertir en bytes
    bytes_data = []
    for i in range(0, len(lsb_bits) - 7, 8):
        byte_val = 0
        for j in range(8):
            byte_val |= (lsb_bits[i + j] << j)
        bytes_data.append(byte_val)
    
    # Le byte à l'index 5 est 123 = '{'
    # Donc le message commence à l'index 5
    # Mais nous voulons "csaw{" donc peut-être que les 4 premiers bytes sont "csaw"
    
    print("Bytes 0-10:", bytes_data[0:11])
    print("Bytes 5-15:", bytes_data[5:16])
    
    # Si le message commence à l'index 5 avec '{', alors peut-être que "csaw" est avant
    # Mais bytes_data[5] = 123 = '{'
    # Donc le message est peut-être "{...}" et "csaw" est ailleurs
    
    # Essayons de voir si le message complet est dans bytes_data
    # Cherchons une séquence de caractères imprimables
    
    # Afficher le texte à partir de l'index 5
    text_from_5 = ''.join(chr(b) if 32 <= b < 127 else '.' for b in bytes_data[5:105])
    print(f"Texte à partir de l'index 5: {text_from_5}")
    
    # Peut-être que le message est encodé différemment - essayons de voir les bits bruts
    # autour de l'index 5
    print(f"Bits LSB autour de l'index 5 (byte 5 = position 40):")
    print(f"Bits 32-55: {lsb_bits[32:56]}")
