import struct

# Re-lisons le pcap pour analyser la structure
with open('capture.pcap', 'rb') as f:
    data = f.read()

# Skip PCAP global header (24 bytes)
offset = 24

packets = []
while offset < len(data):
    # PCAP packet header: ts_sec(4) + ts_usec(4) + incl_len(4) + orig_len(4) = 16 bytes
    if offset + 16 > len(data):
        break
    ts_sec, ts_usec, incl_len, orig_len = struct.unpack('<IIII', data[offset:offset+16])
    offset += 16
    
    if offset + incl_len > len(data):
        break
    
    pkt_data = data[offset:offset+incl_len]
    offset += incl_len
    
    packets.append(pkt_data)

# Cherchons le motif "Se" et extrayons les données
colonne_data = {}  # colonne_id -> liste de (timestamp, data_bytes)

for i, pkt in enumerate(packets):
    se_pos = pkt.find(b'Se')
    if se_pos >= 0:
        # Les 4 octets après "Se"
        if se_pos + 6 <= len(pkt):
            four_bytes = pkt[se_pos+2:se_pos+6]
            # Les 2 premiers octets sont les données, les 2 derniers sont l'ID de colonne
            data_bytes = four_bytes[:2]
            col_id = four_bytes[2] * 256 + four_bytes[3]
            
            if col_id not in colonne_data:
                colonne_data[col_id] = []
            colonne_data[col_id].append((i, data_bytes))

print(f"Nombre de colonnes: {len(colonne_data)}")
for col_id in sorted(colonne_data.keys()):
    entries = colonne_data[col_id]
    print(f"Colonne {col_id}: {len(entries)} entrées - premiers: {entries[:5]}")