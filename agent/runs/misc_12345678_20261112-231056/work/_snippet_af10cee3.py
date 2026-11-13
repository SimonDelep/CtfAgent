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
    
    # Essayer différents bits (pas juste LSB)
    for bit_pos in range(16):
        bits = [(s >> bit_pos) & 1 for s in samples]
        
        # Chercher '{' (bits: 1,1,0,1,1,1,1,0 en LSB first)
        target_bits = [1, 1, 0, 1, 1, 1, 1, 0]
        
        positions = []
        for i in range(len(bits) - len(target_bits)):
            match = True
            for j in range(len(target_bits)):
                if bits[i + j] != target_bits[j]:
                    match = False
                    break
            if match:
                positions.append(i)
        
        if positions:
            print(f"Bit position {bit_pos}: trouvé {len(positions)} occurrences de '{{'")
            # Extraire le message à la première position
            pos = positions[0]
            message_bits = bits[pos:pos + 320]
            message_bytes = []
            for i in range(0, len(message_bits) - 7, 8):
                byte_val = 0
                for j in range(8):
                    byte_val |= (message_bits[i + j] << j)
                message_bytes.append(byte_val)
            
            message_text = ''.join(chr(b) if 32 <= b < 127 else '.' for b in message_bytes)
            print(f"  Message: {message_text[:60]}")
