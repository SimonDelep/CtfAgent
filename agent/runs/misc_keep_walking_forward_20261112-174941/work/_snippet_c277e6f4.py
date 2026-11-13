import struct

def parse_pcapng(filename):
    """Parse un fichier pcapng et retourne les paquets"""
    with open(filename, 'rb') as f:
        data = f.read()
    
    packets = []
    pos = 0
    
    # Section Header Block (SHB)
    if pos + 24 > len(data):
        return packets
    
    block_type = struct.unpack('<H', data[pos:pos+2])[0]
    if block_type != 0x0A0D0D0A:  # SHB
        print(f"Block type: {hex(block_type)}")
        return packets
    
    # Skip SHB
    block_len = struct.unpack('<I', data[pos+4:pos+8])[0]
    pos += block_len
    
    while pos + 20 < len(data):
        block_type = struct.unpack('<I', data[pos:pos+4])[0]
        block_len = struct.unpack('<I', data[pos+4:pos+8])[0]
        
        if block_type == 0x06:  # Interface Description Block
            pos += block_len
            continue
        
        if block_type == 0x09:  # Enhanced Packet Block (EPB)
            # EPB format: block_type(4) + total_len(4) + interface_id(4) + timestamp_hi(4) + timestamp_lo(4) + caplen(4) + origlen(4) + data + padding
            interface_id = struct.unpack('<I', data[pos+8:pos+12])[0]
            ts_hi = struct.unpack('<I', data[pos+12:pos+16])[0]
            ts_lo = struct.unpack('<I', data[pos+16:pos+20])[0]
            caplen = struct.unpack('<I', data[pos+20:pos+24])[0]
            origlen = struct.unpack('<I', data[pos+24:pos+28])[0]
            
            # Data starts at offset 28
            packet_data = data[pos+28:pos+28+caplen]
            
            packets.append({
                'interface_id': interface_id,
                'timestamp': (ts_hi << 32) | ts_lo,
                'caplen': caplen,
                'origlen': origlen,
                'data': packet_data
            })
            
            pos += block_len
        else:
            # Skip unknown block
            if block_len == 0:
                break
            pos += block_len
    
    return packets

packets = parse_pcapng('capture.pcapng')
print(f"Nombre de paquets: {len(packets)}")
for i, p in enumerate(packets[:5]):
    print(f"Paquet {i}: caplen={p['caplen']}, data[:20]={p['data'][:20].hex()}")