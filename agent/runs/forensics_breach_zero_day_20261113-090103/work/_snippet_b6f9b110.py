import struct

# Lire le PCAP et extraire les données TCP du port 8443
with open('fenwick_capture.pcap', 'rb') as f:
    data = f.read()

# Magic number du pcap
magic = struct.unpack('<I', data[:4])[0]
print(f"Magic: {hex(magic)}")

# Parser les paquets
offset = 16  # Skip global header
packets = []

while offset < len(data):
    # Header du paquet (24 octets)
    ts_sec, ts_usec, incl_len, orig_len = struct.unpack('<IIII', data[offset:offset+24])
    offset += 24
    
    # Données du paquet
    pkt_data = data[offset:offset+incl_len]
    offset += incl_len
    
    # Vérifier si c'est un paquet IP (link-type 1 = Ethernet)
    # Skip l'header Ethernet (14 octets)
    if len(pkt_data) > 14:
        eth_type = struct.unpack('>H', pkt_data[12:14])[0]
        if eth_type == 0x0800:  # IPv4
            ip_header = pkt_data[14:34]
            ip_proto = ip_header[9]
            src_ip = '.'.join(str(b) for b in ip_header[12:16])
            dst_ip = '.'.join(str(b) for b in ip_header[16:20])
            
            if ip_proto == 6:  # TCP
                tcp_header = pkt_data[34:54]
                src_port = struct.unpack('>H', tcp_header[0:2])[0]
                dst_port = struct.unpack('>H', tcp_header[2:4])[0]
                
                # Données TCP (skip header TCP)
                data_offset = (tcp_header[12] >> 4) * 4
                tcp_data = pkt_data[34+data_offset:]
                
                if dst_port == 8443 or src_port == 8443:
                    packets.append({
                        'ts': ts_sec + ts_usec/1000000,
                        'src_ip': src_ip,
                        'dst_ip': dst_ip,
                        'src_port': src_port,
                        'dst_port': dst_port,
                        'data': tcp_data
                    })

print(f"\nNombre de paquets TCP sur le port 8443: {len(packets)}")

# Afficher les données des paquets
for i, pkt in enumerate(packets[:10]):
    print(f"\n--- Paquet {i+1} ---")
    print(f"Source: {pkt['src_ip']}:{pkt['src_port']} -> {pkt['dst_ip']}:{pkt['dst_port']}")
    print(f"Data length: {len(pkt['data'])}")
    if pkt['data']:
        # Afficher les premières données en clair si possible
        try:
            text = pkt['data'].decode('utf-8', errors='replace')
            print(f"Data (first 200 chars): {text[:200]}")
        except:
            print(f"Data (hex): {pkt['data'][:50].hex()}")