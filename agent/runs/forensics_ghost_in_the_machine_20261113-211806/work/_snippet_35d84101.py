import struct

with open('capture.pcap', 'rb') as f:
    data = f.read()

marker = b'\xde\xad\xbe\xef'

# Trouver les positions des deadbeef
positions = []
pos = 0
while True:
    idx = data.find(marker, pos)
    if idx == -1:
        break
    positions.append(idx)
    pos = idx + 1

# Premier paquet
first_packet_start = positions[0]  # 40
second_marker = positions[1]  # 46
data_start = second_marker + 4  # 50

# Regardons les 60 octets des données
print("Données du premier paquet (60 octets):")
print(data[data_start:data_start+60].hex())
print()

# Chercher "PING" dans les données
ping_pos = data.find(b'PING', data_start)
print(f"Position de 'PING': {ping_pos}")
print(f"Octets autour de PING: {data[ping_pos-10:ping_pos+10].hex()}")

# L'IP header standard devrait avoir 0x45 comme premier octet
# Chercher 0x45 dans les données
for i in range(data_start, data_start+60):
    if data[i] == 0x45:
        print(f"0x45 trouvé à l'offset {i} (relatif au début des données: {i-data_start})")
        # Afficher 20 octets à partir de là
        print(f"  IP header potentiel: {data[i:i+20].hex()}")