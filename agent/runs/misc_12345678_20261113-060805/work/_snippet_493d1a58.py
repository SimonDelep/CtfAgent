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
    samples_left = []
    samples_right = []
    for i in range(0, len(audio_data), 4):
        if i + 4 <= len(audio_data):
            left = struct.unpack('<h', audio_data[i:i+2])[0]
            right = struct.unpack('<h', audio_data[i+2:i+4])[0]
            samples_left.append(left)
            samples_right.append(right)
    
    # Essayons d'extraire les bits de poids faible (LSB)
    # LSB du canal gauche
    lsb_left = [s & 1 for s in samples_left]
    
    # Regardons les premiers bits
    print("Premiers 100 LSB du canal gauche:")
    print(''.join(str(b) for b in lsb_left[:100]))
    
    # Convertir en octets
    bits = lsb_left
    bytes_list = []
    for i in range(0, len(bits) - 7, 8):
        byte_val = 0
        for j in range(8):
            byte_val |= bits[i + j] << j
        bytes_list.append(byte_val)
    
    print("\nPremiers 50 octets extraits:")
    print(bytes_list[:50])
    
    # Essayer de convertir en texte
    try:
        text = ''.join(chr(b) if 32 <= b < 127 else '.' for b in bytes_list[:200])
        print("\nTexte décodé (premières 200 bytes):")
        print(text)
    except:
        pass