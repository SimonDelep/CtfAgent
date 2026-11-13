import struct

with open("capture.pcapng", 'rb') as f:
    data = f.read()

print(f"Taille du fichier: {len(data)}")

# Header global
magic = struct.unpack('<I', data[0:4])[0]
print(f"Magic: {hex(magic)}")

version_major = struct.unpack('<H', data[4:6])[0]
version_minor = struct.unpack('<H', data[6:8])[0]
print(f"Version: {version_major}.{version_minor}")

thiszone = struct.unpack('<i', data[8:12])[0]
sigfigs = struct.unpack('<I', data[12:16])[0]
snaplen = struct.unpack('<I', data[16:20])[0]
network = struct.unpack('<I', data[20:24])[0]
print(f"Snaplen: {snaplen}, Network: {network}")

# Premier paquet
pos = 24
print(f"\nDébut premier paquet à pos={pos}")
ts_sec = struct.unpack('<I', data[pos:pos+4])[0]
ts_usec = struct.unpack('<I', data[pos+4:pos+8])[0]
incl_len = struct.unpack('<I', data[pos+8:pos+12])[0]
orig_len = struct.unpack('<I', data[pos+12:pos+16])[0]
print(f"ts_sec={ts_sec}, ts_usec={ts_usec}, incl_len={incl_len}, orig_len={orig_len}")

# Données du premier paquet
pkt_data = data[pos+16:pos+16+incl_len]
print(f"Taille données: {len(pkt_data)}")
print(f"Premiers octets: {pkt_data[:50].hex()}")

# Alignement
next_pos = pos + 16 + incl_len
print(f"Prochain paquet devrait être à: {next_pos}")

# Vérifier si aligné sur 4
if incl_len % 4 != 0:
    padding = 4 - (incl_len % 4)
    next_pos += padding
    print(f"Avec padding: {next_pos}")

# Essayer de lire le deuxième paquet
pos2 = next_pos
if pos2 + 16 <= len(data):
    ts_sec2 = struct.unpack('<I', data[pos2:pos2+4])[0]
    ts_usec2 = struct.unpack('<I', data[pos2+4:pos2+8])[0]
    incl_len2 = struct.unpack('<I', data[pos2+8:pos2+12])[0]
    orig_len2 = struct.unpack('<I', data[pos2+12:pos2+16])[0]
    print(f"\nDeuxième paquet: ts_sec={ts_sec2}, incl_len={incl_len2}, orig_len={orig_len2}")
    
    pkt_data2 = data[pos2+16:pos2+16+incl_len2]
    print(f"Taille données2: {len(pkt_data2)}")
    print(f"Premiers octets2: {pkt_data2[:50].hex()}")
