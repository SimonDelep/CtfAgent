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
    
    # Chercher où commence le message en cherchant des caractères imprimables
    # Le flag commence par "csaw{" donc cherchons une séquence de caractères imprimables
    
    # Afficher les premiers bytes bruts
    print("Premiers 100 bytes bruts:")
    print(bytes_data[:100])
    
    # Essayer de trouver une séquence qui ressemble à un flag
    # Cherchons "csaw{" en XOR avec différentes clés
    target = b"csaw{"
    
    for key in range(256):
        # XOR les 5 premiers bytes avec la clé
        xored = [b ^ key for b in bytes_data[:5]]
        if xored == list(target):
            print(f"Clé trouvée: {key} (0x{key:02x})")
            # Déchiffrer tout le message avec cette clé
            decrypted = [b ^ key for b in bytes_data]
            text = ''.join(chr(b) if 32 <= b < 127 else '.' for b in decrypted)
            print(f"Message XOR {key}: {text[:100]}")
            break
