import wave

# Lire le fichier WAV
with wave.open('audio.wav', 'rb') as wf:
    print(f"Channels: {wf.getnchannels()}")
    print(f"Sample width: {wf.getsampwidth()}")
    print(f"Frame rate: {wf.getframerate()}")
    print(f"Num frames: {wf.getnframes()}")
    
    # Lire les données brutes
    data = wf.readframes(wf.getnframes())

print(f"Data length: {len(data)} bytes")

# Si stéréo 16-bit, chaque échantillon fait 2 bytes, et il y a 2 canaux
# Donc chaque frame fait 4 bytes
if wf.getnchannels() == 2 and wf.getsampwidth() == 2:
    # Extraire les canaux
    left_samples = []
    right_samples = []
    
    for i in range(0, len(data), 4):
        if i + 3 < len(data):
            # Little-endian 16-bit signed
            left_val = int.from_bytes(data[i:i+2], 'little', signed=True)
            right_val = int.from_bytes(data[i+2:i+4], 'little', signed=True)
            left_samples.append(left_val)
            right_samples.append(right_val)
    
    print(f"Number of samples per channel: {len(left_samples)}")
    print(f"Left range: {min(left_samples)} to {max(left_samples)}")
    print(f"Right range: {min(right_samples)} to {max(right_samples)}")
    
    # Afficher les premiers échantillons du canal droit
    print(f"First 30 right samples: {right_samples[:30]}")
    
    # Compter les non-zéros
    non_zero = sum(1 for v in right_samples if v != 0)
    print(f"Non-zero right samples: {non_zero} out of {len(right_samples)}")
    
    # Trouver les valeurs uniques dans le canal droit
    unique_vals = set(right_samples)
    print(f"Unique values in right channel: {len(unique_vals)}")
    print(f"Unique values (sorted): {sorted(unique_vals)[:50]}")