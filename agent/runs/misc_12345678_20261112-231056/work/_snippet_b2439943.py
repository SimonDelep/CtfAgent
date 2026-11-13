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
    
    # '{' = 0x7b = 01111011
    # En LSB first: 11011110
    target_char = '{'
    target_bits = []
    byte_val = ord(target_char)
    for bit_idx in range(8):
        target_bits.append((byte_val >> bit_idx) & 1)
    
    print(f"Target bits for '{{': {target_bits}")
    
    # Chercher cette séquence dans lsb_bits
    positions = []
    for i in range(len(lsb_bits) - len(target_bits)):
        match = True
        for j in range(len(target_bits)):
            if lsb_bits[i + j] != target_bits[j]:
                match = False
                break
        if match:
            positions.append(i)
    
    print(f"Positions de '{{' trouvées: {positions[:10]}")
    
    # Pour chaque position, extraire 40 bytes et afficher
    for pos in positions[:5]:
        message_bits = lsb_bits[pos:pos + 320]  # 40 bytes * 8 bits
        message_bytes = []
        for i in range(0, len(message_bits) - 7, 8):
            byte_val = 0
            for j in range(8):
                byte_val |= (message_bits[i + j] << j)
            message_bytes.append(byte_val)
        
        message_text = ''.join(chr(b) if 32 <= b < 127 else '.' for b in message_bytes)
        print(f"Position {pos}: {message_text}")
