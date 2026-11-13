# Les bytes 0-4 sont [0, 22, 24, 138, 191]
# Nous voulons "csaw{" = [99, 115, 97, 119, 123]
# byte 5 = 123 = '{' donc c'est correct

# Cherchons la clé XOR pour bytes 0-4
target = [99, 115, 97, 119]  # "csaw"
data = [0, 22, 24, 138]

print("Recherche de clé XOR:")
for i in range(4):
    key = data[i] ^ target[i]
    print(f"Byte {i}: data={data[i]}, target={target[i]}, key={key} (0x{key:02x})")

# Si la clé est constante, alors tous les keys devraient être égaux
keys = [data[i] ^ target[i] for i in range(4)]
print(f"Keys: {keys}")

# Peut-être que la clé n'est pas constante - essayons de voir le pattern
# Ou peut-être que le message est dans un ordre différent

# Essayons de voir si "csaw" est encodé avec un XOR différent
# Ou peut-être que le message est "csaw{...}" et nous devons trouver où il commence

# Regardons les bytes bruts plus loin
import wave

with wave.open('audio.wav', 'rb') as wf:
    data = wf.readframes(wf.getnframes())
    sampwidth = wf.getsampwidth()
    
    samples = []
    for i in range(0, len(data), sampwidth):
        sample = int.from_bytes(data[i:i+sampwidth], byteorder='little', signed=True)
        samples.append(sample)
    
    lsb_bits = [s & 1 for s in samples]
    
    bytes_data = []
    for i in range(0, len(lsb_bits) - 7, 8):
        byte_val = 0
        for j in range(8):
            byte_val |= (lsb_bits[i + j] << j)
        bytes_data.append(byte_val)
    
    # Cherchons "csaw" dans les bytes_data
    target_bytes = [99, 115, 97, 119]  # "csaw"
    
    positions = []
    for i in range(len(bytes_data) - 4):
        if bytes_data[i:i+4] == target_bytes:
            positions.append(i)
    
    print(f"Positions de 'csaw': {positions[:10]}")
    
    # Cherchons aussi "csaw{"
    target_bytes_full = [99, 115, 97, 119, 123]
    positions_full = []
    for i in range(len(bytes_data) - 5):
        if bytes_data[i:i+5] == target_bytes_full:
            positions_full.append(i)
    
    print(f"Positions de 'csaw{{': {positions_full[:10]}")
