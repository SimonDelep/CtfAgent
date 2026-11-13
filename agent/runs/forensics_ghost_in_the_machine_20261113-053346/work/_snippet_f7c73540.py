import struct

def parse_pcap_raw(pcap_path):
    with open(pcap_path, 'rb') as f:
        magic = struct.unpack('<I', f.read(4))[0]
        print(f"Magic: {hex(magic)}")
        
        if magic == 0xa1b2c3d4:
            endian = '<'
        elif magic == 0xd4c3b2a1:
            endian = '>'
        elif magic == 0xa1b2c3c4:
            # Format nanosecondes peut-être
            endian = '<'
        else:
            print(f"Magic inconnu: {hex(magic)}")
            return []
        
        # Header PCAP (24 bytes)
        f.read(20)  # on saute le reste du header
        
        packets = []
        while True:
            hdr = f.read(16)
            if len(hdr) < 16:
                break
            ts_sec, ts_usec, incl_len, orig_len = struct.unpack(endian + 'IIII', hdr)
            data = f.read(incl_len)
            if len(data) < incl_len:
                break
            
            if len(data) >= 14 + 20 + 8:
                eth = data[:14]
                eth_type = struct.unpack('>H', eth[12:14])[0]
                if eth_type == 0x0800:  # IPv4
                    ip = data[14:34]
                    proto = ip[9]
                    if proto == 17:  # UDP
                        udp = data[34:42]
                        src_port = struct.unpack('>H', udp[0:2])[0]
                        dst_port = struct.unpack('>H', udp[2:4])[0]
                        packets.append((src_port, dst_port))
    return packets

packets = parse_pcap_raw('capture.pcap')
print(f"Total paquets UDP: {len(packets)}")

from collections import Counter
src_ports = [p[0] for p in packets]
counts = Counter(src_ports)

freq_ports = [(port, cnt) for port, cnt in counts.items() if cnt > 1]
singletons = [port for port, cnt in counts.items() if cnt == 1]

print(f"\nPorts fréquents (count > 1): {sorted(freq_ports, key=lambda x: -x[1])[:20]}")
print(f"Nombre de ports fréquents: {len(freq_ports)}")
print(f"Nombre de singletons: {len(singletons)}")

if singletons:
    print(f"\nSingletons triés: {sorted(singletons)}")
    print(f"\nSingletons dans l'ordre d'apparition:")
    seen = set()
    singleton_order = []
    for port in src_ports:
        if counts[port] == 1 and port not in seen:
            singleton_order.append(port)
            seen.add(port)
    print(singleton_order)
    print(f"Total singletons dans l'ordre: {len(singleton_order)}")
