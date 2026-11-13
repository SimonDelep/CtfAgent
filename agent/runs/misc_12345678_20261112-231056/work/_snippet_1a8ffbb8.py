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
    
    # Chercher la séquence binaire de "csaw{"
    # c = 0x63 = 01100011
    # s = 0x73 = 01110011
    # a = 0x61 = 01100001
    # w = 0x77 = 01110111
    # { = 0x7b = 01111011
    
    # En LSB first (bit 0 en premier):
    # c: 11000110 (inversé de 01100011)
    # s: 11001110
    # a: 10000110
    # w: 11101110
    # {: 11011110
    
    target = "csaw{"
    target_bits = []
    for char in target:
        byte_val = ord(char)
        for bit_idx in range(8):
            target_bits.append((byte_val >> bit_idx) & 1)  # LSB first
    
    print(f"Target bits for 'csaw{{': {target_bits}")
    
    # Chercher cette séquence dans lsb_bits
    found_pos = -1
    for i in range(len(lsb_bits) - len(target_bits)):
        match = True
        for j in range(len(target_bits)):
            if lsb_bits[i + j] != target_bits[j]:
                match = False
                break
        if match:
            found_pos = i
            break
    
    print(f"Position de 'csaw{{' trouvée à: {found_pos}")
    
    if found_pos >= 0:
        # Extraire le message à partir de cette position
        message_bits = lsb_bits[found_pos:found_pos + 200]
        
        # Convertir en bytes
        message_bytes = []
        for i in range(0, len(message_bits) - 7, 8):
            byte_val = 0
            for j in range(8):
                byte_val |= (message_bits[i + j] << j)
            message_bytes.append(byte_val)
        
        message_text = ''.join(chr(b) if 32 <= b < 127 else '.' for b in message_bytes)
        print(f"Message à partir de la position trouvée: {message_text}")
        
        # Afficher les bytes bruts
        print(f"Bytes bruts: {message_bytes[:50]}")
