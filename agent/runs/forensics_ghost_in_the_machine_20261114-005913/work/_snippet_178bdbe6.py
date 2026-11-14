with open('capture.pcap', 'rb') as f:
    data = f.read()

# Offset IP header = 54
ip_header = data[54:74]
print(f"IP header: {ip_header.hex()}")

# Port source UDP est à offset 0:2 du UDP header
# UDP header commence à 54 + 20 = 74
udp_header = data[74:82]
print(f"UDP header: {udp_header.hex()}")

src_port = int.from_bytes(udp_header[0:2], 'big')
dst_port = int.from_bytes(udp_header[2:4], 'big')
print(f"Port source UDP: {src_port}")
print(f"Port dest UDP: {dst_port}")

# Payload
udp_len = int.from_bytes(udp_header[4:6], 'big')
print(f"UDP length: {udp_len}")
payload = data[82:82+udp_len-8]
print(f"Payload: {payload}")