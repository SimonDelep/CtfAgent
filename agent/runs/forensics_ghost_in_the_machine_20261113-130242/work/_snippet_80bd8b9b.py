import struct

with open('capture.pcap', 'rb') as f:
    data = f.read()

# Header PCAP standard: 24 octets
# Ensuite, chaque paquet a:
# - 16 octets de header PCAP (ts_sec, ts_usec, incl_len, orig_len)
# - Les données du paquet

# Analysons la structure des données
offset = 24  # après header PCAP

# Premier header de paquet
header1 = data[offset:offset+16]
print(f"Header paquet 1: {header1.hex()}")
ts_sec = struct.unpack('<I', header1[0:4])[0]
ts_usec = struct.unpack('<I', header1[4:8])[0]
incl_len = struct.unpack('<I', header1[8:12])[0]
orig_len = struct.unpack('<I', header1[12:16])[0]
print(f"  ts_sec={ts_sec}, ts_usec={ts_usec}, incl_len={incl_len}, orig_len={orig_len}")

# Les données du paquet commencent à offset+16
packet_data = data[offset+16:offset+16+incl_len]
print(f"Données du paquet ({incl_len} octets): {packet_data.hex()}")

# Chercher deadbeef dans les données
idx = packet_data.find(b'\xde\xad\xbe\xef')
print(f"deadbeef à l'offset {idx} dans les données du paquet")

# Regarder la structure après deadbeef
if idx >= 0:
    print(f"Après deadbeef: {packet_data[idx:idx+50].hex()}")
