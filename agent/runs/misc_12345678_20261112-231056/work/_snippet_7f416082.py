import wave

# Ouvrir le fichier WAV
with wave.open('audio.wav', 'rb') as wf:
    data = wf.readframes(wf.getnframes())
    sampwidth = wf.getsampwidth()
    
    # Extraire les échantillons par canal
    left_samples = []
    right_samples = []
    
    for i in range(0, len(data), sampwidth * 2):
        left = int.from_bytes(data[i:i+sampwidth], byteorder='little', signed=True)
        right = int.from_bytes(data[i+sampwidth:i+sampwidth*2], byteorder='little', signed=True)
        left_samples.append(left)
        right_samples.append(right)
    
    # Essayer: différence entre canaux
    diff_samples = [abs(l - r) for l, r in zip(left_samples, right_samples)]
    
    # Extraire LSB de la différence
    diff_lsb = [s & 1 for s in diff_samples]
    
    # Chercher '{'
    target_bits = [1, 1, 0, 1, 1, 1, 1, 0]
    positions = []
    for i in range(len(diff_lsb) - len(target_bits)):
        match = True
        for j in range(len(target_bits)):
            if diff_lsb[i + j] != target_bits[j]:
                match = False
                break
        if match:
            positions.append(i)
    
    print(f"Positions de '{{' dans diff LSB: {positions[:10]}")
    
    # Extraire message à la première position
    if positions:
        pos = positions[0]
        message_bits = diff_lsb[pos:pos + 320]
        message_bytes = []
        for i in range(0, len(message_bits) - 7, 8):
            byte_val = 0
            for j in range(8):
                byte_val |= (message_bits[i + j] << j)
            message_bytes.append(byte_val)
        
        message_text = ''.join(chr(b) if 32 <= b < 127 else '.' for b in message_bytes)
        print(f"Message diff LSB: {message_text}")
    
    # Essayer: somme des canaux
    sum_samples = [abs(l + r) for l, r in zip(left_samples, right_samples)]
    sum_lsb = [s & 1 for s in sum_samples]
    
    positions_sum = []
    for i in range(len(sum_lsb) - len(target_bits)):
        match = True
        for j in range(len(target_bits)):
            if sum_lsb[i + j] != target_bits[j]:
                match = False
                break
        if match:
            positions_sum.append(i)
    
    print(f"Positions de '{{' dans sum LSB: {positions_sum[:10]}")
