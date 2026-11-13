import struct

# Re-lire le pcap
with open('capture.pcap', 'rb') as f:
    f.read(24)
    
    packets = []
    while True:
        ts_sec = f.read(4)
        if len(ts_sec) < 4:
            break
        ts_sec = struct.unpack('<I', ts_sec)[0]
        ts_usec = struct.unpack('<I', f.read(4))[0]
        incl_len = struct.unpack('<I', f.read(4))[0]
        orig_len = struct.unpack('<I', f.read(4))[0]
        
        data = f.read(incl_len)
        
        if len(data) >= 42:
            udp = data[34:42]
            udp_src_port = struct.unpack('>H', udp[0:2])[0]
            packets.append(udp_src_port)

from collections import Counter
port_counts = Counter(packets)

# Extraire les singletons dans l'ordre
singletons_in_order = [p for p in packets if port_counts[p] == 1]

# Peut-être que le message est dans les différences entre ports consécutifs?
diffs = [singletons_in_order[i+1] - singletons_in_order[i] for i in range(len(singletons_in_order)-1)]
print(f"Differences entre singletons consécutifs (first 30): {diffs[:30]}")

# Ou peut-être que les singletons sont des indices vers quelque chose
# Regardons si les singletons, quand on prend le modulo de quelque chose, donnent des lettres
# Essayons modulo 256
mods_256 = [p % 256 for p in singletons_in_order]
print(f"\nSingletons mod 256 (first 30): {mods_256[:30]}")

# Essayons de voir si c'est du texte XORé
# Peut-être que le XOR key est dans les ports fréquents
# Les ports fréquents sont: 40052, 40100, 40104, 40111, 40115, 40119, 50608, 50631, 50972
# Leurs low bytes: 116, 164, 168, 175, 179, 183, 176, 199, 28

# Peut-être que le message est XORé avec une clé répétitive
# Essayons de XORer les singletons avec différentes clés

# D'abord, regardons si les singletons mod 256 forment un motif
print(f"\nSingletons mod 256 (tous): {mods_256}")

# Essayons de convertir en ASCII
try:
    msg = bytes(mods_256).decode('ascii', errors='replace')
    print(f"Message (mod 256): {msg}")
except:
    pass
