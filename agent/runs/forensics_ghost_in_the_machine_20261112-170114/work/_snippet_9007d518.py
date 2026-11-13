import struct

# Lecture du fichier PCAP
with open('capture.pcap', 'rb') as f:
    # En-tête PCAP global
    magic = struct.unpack('<I', f.read(4))[0]
    print(f"Magic: 0x{magic:08x}")
    
    version_major, version_minor = struct.unpack('<HH', f.read(4))
    print(f"Version: {version_major}.{version_minor}")
    
    thiszone, sigfigs, snaplen = struct.unpack('<III', f.read(12))
    print(f"thiszone={thiszone}, sigfigs={sigfigs}, snaplen={snaplen}")
    
    network = struct.unpack('<I', f.read(4))[0]
    print(f"Link type: {network}")
    
    # Link type 1 = Ethernet
    # Link type 228 = Linux SLL
    # Link type 101 = Raw IP
    
    # Lisons quelques paquets
    for i in range(10):
        ts_sec, ts_usec, incl_len, orig_len = struct.unpack('<IIII', f.read(16))
        packet = f.read(incl_len)
        print(f"\nPacket {i}: len={incl_len}, ts={ts_sec}.{ts_usec}")
        
        # En-tête Ethernet (14 octets)
        if len(packet) >= 14:
            eth_dst = packet[0:6]
            eth_src = packet[6:12]
            eth_type = struct.unpack('>H', packet[12:14])[0]
            print(f"  Ether type: 0x{eth_type:04x}")
            
            if eth_type == 0x0800:  # IPv4
                ip = packet[14:]
                ip_ver_ihl = ip[0]
                ip_version = (ip_ver_ihl >> 4) & 0xF
                ip_ihl = (ip_ver_ihl & 0xF) * 4
                ip_proto = ip[9]
                print(f"  IP proto: {ip_proto}")
                
                if ip_proto == 1:  # ICMP
                    icmp = packet[14 + ip_ihl:]
                    icmp_type = icmp[0]
                    icmp_code = icmp[1]
                    print(f"  ICMP type={icmp_type}, code={icmp_code}")
                    
                    # Payload ICMP
                    if len(icmp) > 8:
                        payload = icmp[8:]
                        print(f"  ICMP payload ({len(payload)} bytes): {payload[:50].hex()}")
                        # Essayons de lire comme ASCII
                        try:
                            ascii_payload = payload[:50].decode('ascii', errors='replace')
                            print(f"  ASCII: {ascii_payload}")
                        except:
                            pass
