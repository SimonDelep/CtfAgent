import struct

with open('capture.pcap', 'rb') as f:
    data = f.read()

dead_beef = bytes.fromhex('deadbeef')
positions = []
pos = 0
while True:
    idx = data.find(dead_beef, pos)
    if idx == -1:
        break
    positions.append(idx)
    pos = idx + 1

# La structure semble être:
# [deadbeef] [2 octets] [deadbeef] [paquet IP/UDP] [8 octets] [deadbeef] ...
# Donc les positions de marqueurs sont: 0, 6, 6+2+taille_paquet+8, ...

# Trouvons la taille du paquet IP/UDP
# Entre position 6 (deuxième marqueur du premier paquet) et position 102 (premier marqueur du deuxième paquet)
# Il y a: 2 octets (déjà comptés) + paquet IP/UDP + 8 octets

# Position 6 est le deuxième marqueur du premier paquet
# Position 102 est le premier marqueur du deuxième paquet
# Donc entre 6 et 102, il y a: paquet IP/UDP + 8 octets

print(f"Position 6: {positions[1]}")
print(f"Position 102: {positions[2]}")

# Entre positions[1] et positions[2], il y a positions[2] - positions[1] - 4 (taille du marqueur)
# Mais positions[1] est le début du deuxième marqueur, donc après positions[1]+4, on a les données

# En fait, regardons: positions[1] = 46 (deuxième marqueur du premier paquet)
# positions[2] = 102 (premier marqueur du deuxième paquet)
# Donc entre 46 et 102, il y a 56 octets
# Ces 56 octets contiennent: le paquet IP/UDP + 8 octets de fin

# Vérifions: 56 - 8 = 48 octets pour le paquet IP/UDP
print(f"Distance entre positions[1] et positions[2]: {positions[2] - positions[1]}")

# Regardons les données entre positions[1]+4 et positions[2]
start = positions[1] + 4
end = positions[2]
print(f"Données entre marqueurs 1 et 2: {data[start:end].hex()}")
print(f"Longueur: {end - start}")

# Le paquet IP commence par 0001080045...
# 00 01 = peut-être une version ou type
# 08 00 = EtherType IP (0x0800)
# 45 = version IP 4, header length 5 (20 octets)
# 00 20 = longueur totale du paquet IP (32 octets)

# Donc le paquet IP fait 32 octets, plus l'en-tête Ethernet?
# En fait, dans un fichier pcap, on peut avoir différents liens
# Ici, il semble y avoir un en-tête de 2 octets avant le paquet IP

# Analysons le paquet IP
ip_start = start + 2  # sauter les 2 premiers octets (00 01)
ip_data = data[ip_start:end-8]  # sauter les 8 octets de fin
print(f"\nDonnées IP: {ip_data.hex()}")
print(f"Longueur IP: {len(ip_data)}")

# Décomposons l'en-tête IP
if len(ip_data) >= 20:
    version_ihl = ip_data[0]
    version = version_ihl >> 4
    ihl = (version_ihl & 0x0F) * 4
    total_length = struct.unpack('>H', ip_data[2:4])[0]
    protocol = ip_data[9]
    src_ip = '.'.join(str(b) for b in ip_data[12:16])
    dst_ip = '.'.join(str(b) for b in ip_data[16:20])
    
    print(f"Version IP: {version}")
    print(f"IHL: {ihl}")
    print(f"Longueur totale: {total_length}")
    print(f"Protocole: {protocol} (17 = UDP)")
    print(f"Source IP: {src_ip}")
    print(f"Dest IP: {dst_ip}")
    
    # En-tête UDP commence après l'en-tête IP
    udp_start = ip_start + ihl
    udp_data = data[udp_start:udp_start+8]  # 8 octets d'en-tête UDP
    print(f"\nDonnées UDP: {udp_data.hex()}")
    
    if len(udp_data) >= 8:
        src_port = struct.unpack('>H', udp_data[0:2])[0]
        dst_port = struct.unpack('>H', udp_data[2:4])[0]
        udp_length = struct.unpack('>H', udp_data[4:6])[0]
        print(f"Port source: {src_port}")
        print(f"Port destination: {dst_port}")
        print(f"Longueur UDP: {udp_length}")