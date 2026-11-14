with open('capture.pcap', 'rb') as f:
    data = f.read()

# Premier IP à position 54
ip_start = 54
print(f"IP header à partir de {ip_start}:")
print(f"Positions {ip_start}-{ip_start+28}: {data[ip_start:ip_start+28].hex()}")

# IP header:
# 0x45 = version 4, IHL 5 (20 octets)
# Octets 12-15: source IP
# Octets 16-19: dest IP

src_ip = data[ip_start+12:ip_start+16]
dst_ip = data[ip_start+16:ip_start+20]
print(f"Source IP: {src_ip.hex()}")
print(f"Dest IP: {dst_ip.hex()}")

# Convertir en notation pointée
src_ip_str = '.'.join(str(b) for b in src_ip)
dst_ip_str = '.'.join(str(b) for b in dst_ip)
print(f"Source IP: {src_ip_str}")
print(f"Dest IP: {dst_ip_str}")

# UDP header commence à ip_start + 20
udp_start = ip_start + 20
print(f"\nUDP header à partir de {udp_start}:")
print(f"Positions {udp_start}-{udp_start+16}: {data[udp_start:udp_start+16].hex()}")

src_port = int.from_bytes(data[udp_start:udp_start+2], 'big')
dst_port = int.from_bytes(data[udp_start+2:udp_start+4], 'big')
length = int.from_bytes(data[udp_start+4:udp_start+6], 'big')
checksum = int.from_bytes(data[udp_start+6:udp_start+8], 'big')

print(f"Src port: {src_port}")
print(f"Dst port: {dst_port}")
print(f"Length: {length}")
print(f"Checksum: {checksum}")

# Payload UDP
payload_start = udp_start + 8
print(f"\nPayload à partir de {payload_start}:")
print(f"Positions {payload_start}-{payload_start+20}: {data[payload_start:payload_start+20].hex()}")
print(f"Payload (repr): {data[payload_start:payload_start+20]}")
