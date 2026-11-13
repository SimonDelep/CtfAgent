import struct

with open('capture.pcap', 'rb') as f:
    data = f.read()

# Premier paquet
offset = 24
header = data[offset:offset+16]
incl_len = struct.unpack('<I', header[8:12])[0]
print(f"Longueur du paquet: {incl_len}")

packet_data = data[offset+16:offset+16+incl_len]
print(f"Données du paquet ({incl_len} octets): {packet_data.hex()}")

# deadbeef 0002 deadbeef 0001 (12 octets)
# Ensuite IP header
ip_start = 12
print(f"IP header: {packet_data[ip_start:ip_start+20].hex()}")

# Version/IHL
ver_ihl = packet_data[ip_start]
version = (ver_ihl >> 4) & 0xF
ihl = (ver_ihl & 0xF) * 4
print(f"Version: {version}, IHL: {ihl} octets")

# Longueur totale
total_len = struct.unpack('>H', packet_data[ip_start+2:ip_start+4])[0]
print(f"Longueur totale IP: {total_len}")

# TTL, protocole
ttl = packet_data[ip_start+8]
protocol = packet_data[ip_start+9]
print(f"TTL: {ttl}, Protocole: {protocol}")

# Checksum IP
checksum_ip = struct.unpack('>H', packet_data[ip_start+10:ip_start+12])[0]
print(f"Checksum IP: {checksum_ip:04x}")

# Adresses IP
src_ip = '.'.join(str(b) for b in packet_data[ip_start+12:ip_start+16])
dst_ip = '.'.join(str(b) for b in packet_data[ip_start+16:ip_start+20])
print(f"Src IP: {src_ip}, Dst IP: {dst_ip}")

# UDP start
udp_start = ip_start + ihl
print(f"UDP start offset: {udp_start}")
print(f"Données UDP: {packet_data[udp_start:].hex()}")
