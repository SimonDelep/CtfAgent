import struct

# Lire le PCAP
with open('capture.pcap', 'rb') as f:
    data = f.read()

# Header global (24 octets)
# On ignore le magic corrompu, on parse directement
offset = 24

packets = []
while offset < len(data):
    if offset + 16 > len(data):
        break
    ts_sec, ts_usec, incl_len, orig_len = struct.unpack('<IIII', data[offset:offset+16])
    offset += 16
    
    if offset + incl_len > len(data):
        break
    
    pkt_data = data[offset:offset+incl_len]
    offset += incl_len
    
    packets.append((ts_sec, ts_usec, pkt_data))

print(f"Nombre de paquets: {len(packets)}")

# Analyser la structure de chaque paquet
# Chaque paquet semble avoir:
# - deadbeef (4 octets)
# - 0002 (2 octets)
# - deadbeef (4 octets)
# - 0001 (2 octets)
# - 0800 (2 octets) - type Ethernet?
# - 4500... (IP header)

# On veut trouver les positions variables
# Regardons tous les paquets et identifions les positions qui varient

# Extraire les bytes de chaque paquet après le header Ethernet/IP
# On va regarder les 46 octets de chaque paquet

# Trouver les positions qui varient
positions_variées = set()
for i in range(len(packets)):
    for j in range(len(packets[0][2])):
        if i == 0:
            continue
        if packets[i][2][j] != packets[0][2][j]:
            positions_variées.add(j)

print(f"Positions qui varient: {sorted(positions_variées)}")

# Afficher les valeurs à ces positions pour quelques paquets
print("\nValeurs aux positions variables pour les 10 premiers paquets:")
for i in range(min(10, len(packets))):
    pkt = packets[i][2]
    vals = {pos: pkt[pos] for pos in sorted(positions_variées)}
    print(f"Paquet {i}: {vals}")