import struct

# Lire le fichier WAV
with open('audio.wav', 'rb') as f:
    data = f.read()

# Trouver le chunk 'data'
data_start = data.find(b'data')
if data_start != -1:
    data_start += 8
    audio_data = data[data_start:]
    
    # C'est stéréo, donc alternance canal gauche/droite
    # Extraire les échantillons par canal
    left_samples = []
    right_samples = []
    
    for i in range(0, len(audio_data), 4):  # 4 bytes par frame (2 canaux * 2 bytes)
        if i + 4 <= len(audio_data):
            left = struct.unpack('<h', audio_data[i:i+2])[0]
            right = struct.unpack('<h', audio_data[i+2:i+4])[0]
            left_samples.append(left)
            right_samples.append(right)
    
    print("Nombre d'échantillons par canal:", len(left_samples))
    
    # Essayer LSB sur chaque canal séparément
    def extract_lsb_bytes(samples, name):
        lsb_bits = [s & 1 for s in samples]
        bytes_from_lsb = []
        for i in range(0, len(lsb_bits) - 7, 8):
            byte_val = 0
            for j in range(8):
                byte_val |= (lsb_bits[i + j] << j)
            bytes_from_lsb.append(byte_val)
        return bytes(bytes_from_lsb)
    
    left_bytes = extract_lsb_bytes(left_samples, "left")
    right_bytes = extract_lsb_bytes(right_samples, "right")
    
    print("\nCanal gauche (premiers 200 bytes):")
    print(left_bytes[:200])
    
    print("\nCanal droit (premiers 200 bytes):")
    print(right_bytes[:200])
    
    # Chercher 'csaw{' dans chaque canal
    for name, data_bytes in [("left", left_bytes), ("right", right_bytes)]:
        idx = data_bytes.find(b'csaw{')
        if idx != -1:
            print(f"\nTrouvé 'csaw{{' dans {name} a l'index {idx}")
            print("Contexte:", data_bytes[idx:idx+100])