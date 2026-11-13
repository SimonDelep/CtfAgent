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
    
    # Chercher "csaw{" en MSB first (ordre normal des bits)
    target = "csaw{"
    target_bits_msb = []
    for char in target:
        byte_val = ord(char)
        for bit_idx in range(7, -1, -1):  # MSB first
            target_bits_msb.append((byte_val >> bit_idx) & 1)
    
    print(f"Target bits MSB first for 'csaw{{': {target_bits_msb}")
    
    # Chercher cette séquence
    positions = []
    for i in range(len(lsb_bits) - len(target_bits_msb)):
        match = True
        for j in range(len(target_bits_msb)):
            if lsb_bits[i + j] != target_bits_msb[j]:
                match = False
                break
        if match:
            positions.append(i)
    
    print(f"Positions de 'csaw{{' (MSB first) trouvées: {positions[:10]}")
    
    # Chercher aussi en LSB first
    target_bits_lsb = []
    for char in target:
        byte_val = ord(char)
        for bit_idx in range(8):  # LSB first
            target_bits_lsb.append((byte_val >> bit_idx) & 1)
    
    positions_lsb = []
    for i in range(len(lsb_bits) - len(target_bits_lsb)):
        match = True
        for j in range(len(target_bits_lsb)):
            if lsb_bits[i + j] != target_bits_lsb[j]:
                match = False
                break
        if match:
            positions_lsb.append(i)
    
    print(f"Positions de 'csaw{{' (LSB first) trouvées: {positions_lsb[:10]}")
