import struct

# Lire le fichier audio
with open('audio.wav', 'rb') as f:
    data = f.read()

# Trouver le chunk data
data_start = data.find(b'data')
if data_start >= 0:
    data_size = int.from_bytes(data[data_start+4:data_start+8], 'little')
    audio_data = data[data_start+8:data_start+8+data_size]
    print(f"Données audio: {len(audio_data)} octets")
    
    # Le format est 16-bit stéréo, donc chaque échantillon est 2 octets
    # Nombre d'échantillons = data_size / 2
    num_samples = len(audio_data) // 2
    print(f"Nombre d'échantillons: {num_samples}")
    
    # Extraire les LSB de chaque échantillon
    lsb_bits = []
    for i in range(0, len(audio_data), 2):
        sample = struct.unpack('<h', audio_data[i:i+2])[0]
        lsb_bits.append(sample & 1)
    
    # Convertir les bits en bytes
    lsb_bytes = []
    for i in range(0, len(lsb_bits), 8):
        byte_val = 0
        for j in range(8):
            if i+j < len(lsb_bits):
                byte_val |= (lsb_bits[i+j] << j)
        lsb_bytes.append(byte_val)
    
    lsb_data = bytes(lsb_bytes)
    print(f"Données LSB: {len(lsb_data)} octets")
    print(f"Premiers 100 octets (hex): {lsb_data[:100].hex()}")
    print(f"Contenu brut: {lsb_data[:100]}")
    
    # Chercher des strings imprimables
    import re
    strings = re.findall(rb'[\x20-\x7e]{4,}', lsb_data)
    print(f"\nStrings trouvées dans LSB:")
    for s in strings[:20]:
        print(f"  {s}")