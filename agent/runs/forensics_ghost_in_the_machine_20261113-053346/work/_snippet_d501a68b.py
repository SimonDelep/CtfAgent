import struct
import os

# Parser le PCAP manuellement pour extraire les ports sources UDP
def parse_pcap_raw(pcap_path):
    with open(pcap_path, 'rb') as f:
        # Header PCAP (24 bytes)
        magic = struct.unpack('<I', f.read(4))[0]
        if magic == 0xa1b2c3d4:
            endian = '<'
        elif magic == 0xd4c3b2a1:
            endian = '>'
        else:
            print(f"Magic inconnu: {hex(magic)}")
            return []
        
        # Version, zone, précision, snaplen, lien
        f.read(20)  # on saute le reste du header
        
        packets = []
        while True:
            # Header paquet (16 bytes)
            hdr = f.read(16)
            if len(hdr) < 16:
                break
            ts_sec, ts_usec, incl_len, orig_len = struct.unpack(endian + 'IIII', hdr)
            data = f.read(incl_len)
            if len(data) < incl_len:
                break
            
            # Lien Ethernet (14 bytes) + IP (20 bytes minimum) + UDP (8 bytes)
            # On suppose Ethernet II
            if len(data) >= 14 + 20 + 8:
                # Skip Ethernet header (14 bytes)
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
print(f"Total paquets: {len(packets)}")

# Compter les ports sources
from collections import Counter
src_ports = [p[0] for p in packets]
counts = Counter(src_ports)

# Trouver les ports fréquents et les singletons
freq_ports = [(port, cnt) for port, cnt in counts.items() if cnt > 1]
singletons = [port for port, cnt in counts.items() if cnt == 1]

print(f"\nPorts fréquents (count > 1): {sorted(freq_ports, key=lambda x: -x[1])[:20]}")
print(f"Nombre de ports fréquents: {len(freq_ports)}")
print(f"Nombre de singletons: {len(singletons)}")
print(f"\nSingletons (triés): {sorted(singletons)}")
print(f"\nSingletons dans l'ordre d'apparition:")
seen = set()
singleton_order = []
for port in src_ports:
    if counts[port] == 1 and port not in seen:
        singleton_order.append(port)
        seen.add(port)
print(singleton_order[:30])
print(f"... total {len(singleton_order)}")
