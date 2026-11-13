import struct

# Lire le fichier WAV
with open('audio.wav', 'rb') as f:
    riff = f.read(4)
    file_size = struct.unpack('<I', f.read(4))[0]
    wave = f.read(4)
    
    # Trouver le chunk fmt
    while True:
        chunk_id = f.read(4)
        chunk_size = struct.unpack('<I', f.read(4))[0]
        if chunk_id == b'fmt ':
            fmt_data = f.read(chunk_size)
            audio_format, num_channels, sample_rate, _, _, bits_per_sample = struct.unpack('<HHIIHH', fmt_data)
            break
        else:
            f.seek(chunk_size, 1)
    
    # Trouver le chunk data
    while True:
        chunk_id = f.read(4)
        chunk_size = struct.unpack('<I', f.read(4))[0]
        if chunk_id == b'data':
            break
        else:
            f.seek(chunk_size, 1)
    
    data = f.read(chunk_size)

print(f"WAV Info: {num_channels} channels, {sample_rate} Hz, {bits_per_sample} bits, {len(data)} bytes")

# Extraire les échantillons
samples = struct.unpack('<' + 'h' * (len(data) // 2), data)
print(f"Total samples: {len(samples)}")

# Extraire LSB de chaque échantillon
lsb_bits = [s & 1 for s in samples]

# Regrouper par 8 pour former des bytes
lsb_bytes = []
for i in range(0, len(lsb_bits) - 7, 8):
    byte_val = 0
    for j in range(8):
        byte_val |= (lsb_bits[i + j] << j)
    lsb_bytes.append(byte_val)

print(f"LSB bytes count: {len(lsb_bytes)}")
print(f"First 100 LSB bytes: {bytes(lsb_bytes[:100])}")
print(f"First 100 LSB bytes (hex): {bytes(lsb_bytes[:100]).hex()}")

# Essayer de trouver des chaînes imprimables
printable = ''.join(chr(b) if 32 <= b < 127 else '.' for b in lsb_bytes[:500])
print(f"LSB printable (first 500): {printable}")