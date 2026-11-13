import struct

# Lire le fichier WAV
with open('audio.wav', 'rb') as f:
    data = f.read()

# Header WAV
print("Header:", data[:44])
print("Format:", struct.unpack('<H', data[20:22])[0])
print("Channels:", struct.unpack('<H', data[22:24])[0])
print("SampleRate:", struct.unpack('<I', data[24:28])[0])
print("BytesPerSec:", struct.unpack('<I', data[28:32])[0])
print("BlockAlign:", struct.unpack('<H', data[32:34])[0])
print("BitsPerSample:", struct.unpack('<H', data[34:36])[0])

# Trouver le chunk 'data'
idx = data.find(b'data')
print("Data chunk at:", idx)
if idx > 0:
    data_size = struct.unpack('<I', data[idx+4:idx+8])[0]
    print("Data size:", data_size)
    audio_data = data[idx+8:idx+8+data_size]
    print("First 100 bytes of audio:", list(audio_data[:100]))