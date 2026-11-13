import struct

# Lire le fichier WAV
with open('audio.wav', 'rb') as f:
    data = f.read()

# Trouver le chunk 'data'
data_start = data.find(b'data')
if data_start != -1:
    data_start += 8  # Après 'data' et la taille
    audio_data = data[data_start:]
    print(f"Taille des données audio: {len(audio_data)} bytes")
    
    # C'est du PCM 16-bit stéréo, donc 2 canaux * 2 bytes = 4 bytes par échantillon temporel
    # Mais en fait c'est 2 échantillons de 16 bits par frame (stéréo)
    # Chaque échantillon est 2 bytes (int16)
    
    # Extraire tous les échantillons
    samples = []
    for i in range(0, len(audio_data), 2):
        if i + 2 <= len(audio_data):
            val = struct.unpack('<h', audio_data[i:i+2])[0]
            samples.append(val)
    
    print(f"Nombre d'échantillons: {len(samples)}")
    
    # Regarder les LSB de chaque échantillon
    lsb_bits = [s & 1 for s in samples]
    
    # Essayer de convertir en bytes (8 bits = 1 byte)
    bytes_from_lsb = []
    for i in range(0, len(lsb_bits) - 7, 8):
        byte_val = 0
        for j in range(8):
            byte_val |= (lsb_bits[i + j] << j)
        bytes_from_lsb.append(byte_val)
    
    # Afficher les premiers bytes en ASCII
    result = ''.join(chr(b) if 32 <= b < 127 else '.' for b in bytes_from_lsb[:200])
    print("LSB (little-endian bit order):")
    print(result)
    
    # Essayer aussi big-endian bit order
    bytes_from_lsb_be = []
    for i in range(0, len(lsb_bits) - 7, 8):
        byte_val = 0
        for j in range(8):
            byte_val |= (lsb_bits[i + j] << (7 - j))
        bytes_from_lsb_be.append(byte_val)
    
    result_be = ''.join(chr(b) if 32 <= b < 127 else '.' for b in bytes_from_lsb_be[:200])
    print("\nLSB (big-endian bit order):")
    print(result_be)