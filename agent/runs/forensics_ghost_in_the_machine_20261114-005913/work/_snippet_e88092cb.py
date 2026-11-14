with open('capture.pcap', 'rb') as f:
    data = f.read()

# Premier paquet: positions[0]=40, positions[1]=46
# deadbeef à 40, 2 octets à 44, deadbeef à 46, 4 octets à 50, IP à 54

print("Analyse du premier paquet:")
print(f"deadbeef1 à 40: {data[40:44].hex()}")
print(f"2 octets à 44: {data[44:46].hex()}")
print(f"deadbeef2 à 46: {data[46:50].hex()}")
print(f"4 octets méta à 50: {data[50:54].hex()}")
print(f"IP header à 54: {data[54:74].hex()}")

# IP header: version/IHL à l'octet 0, total length à 2-3, etc.
ip_header = data[54:74]
print(f"\nIP header bytes: {ip_header.hex()}")
print(f"Version/IHL: {ip_header[0]:02x}")
print(f"Total length: {int.from_bytes(ip_header[2:4], 'big')}")

# Port source est à offset 20:22 dans l'IP header
src_port = int.from_bytes(ip_header[20:22], 'big')
dst_port = int.from_bytes(ip_header[22:24], 'big')
print(f"Port source: {src_port}")
print(f"Port dest: {dst_port}")

# UDP header commence à offset 20 dans l'IP header (IP header = 20 octets)
# Donc UDP header est à 54 + 20 = 74
udp_header = data[74:82]
print(f"\nUDP header: {udp_header.hex()}")
udp_len = int.from_bytes(udp_header[4:6], 'big')
print(f"UDP length: {udp_len}")

# Payload UDP
payload = data[82:82+udp_len-8]
print(f"Payload: {payload}")