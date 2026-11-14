import struct

# Lire le fichier
with open('capture.pcap', 'rb') as f:
    data = f.read()

# Magic number
magic = data[:4]
print(f"Magic: {magic.hex()}")

# En-tête global (24 octets ou plus)
# On cherche le premier "dead beef"
deadbeef = b'\xde\xad\xbe\xef'
first_db = data.find(deadbeef)
print(f"Premier deadbeef à l'offset: {first_db}")

# En-tête global = first_db octets
print(f"En-tête global: {data[:first_db].hex()}")

# Maintenant parser les paquets
# Structure: deadbeef + 2 octets + deadbeef + données
offset = first_db
packets = []
while offset < len(data):
    if data[offset:offset+4] != deadbeef:
        break
    # deadbeef (4)
    offset += 4
    # 2 octets
    offset += 2
    # deadbeef (4)
    offset += 4
    # Maintenant c'est les données du paquet
    # On cherche le prochain deadbeef pour savoir la fin de ce paquet
    next_db = data.find(deadbeef, offset)
    if next_db == -1:
        packet_data = data[offset:]
        offset = len(data)
    else:
        packet_data = data[offset:next_db]
        offset = next_db
    
    packets.append(packet_data)

print(f"Nombre de paquets: {len(packets)}")

# Extraire les ports sources
# Structure du paquet: 0800 4500 ... (IP header)
# IP header commence après "0800" (2 octets)
# Port source est à offset 20+20=40 depuis le début de l'IP header

ports = []
for i, pkt in enumerate(packets):
    # Trouver le début de l'IP header (après "0800")
    # Le paquet commence après les marqueurs deadbeef
    # On cherche "4500" qui est le début de l'IP header
    ip_start = pkt.find(b'\x45\x00')
    if ip_start == -1:
        print(f"Paquet {i}: pas d'IP header trouvé")
        continue
    
    # IP header length (IHL) est le premier octet >> 4 * 4
    ihl = pkt[ip_start] & 0x0F
    ip_header_len = ihl * 4
    
    # Port source est à offset ip_start + ip_header_len + 2 (port source est les 2 premiers octets de UDP)
    src_port_offset = ip_start + ip_header_len
    if src_port_offset + 2 <= len(pkt):
        src_port = struct.unpack('>H', pkt[src_port_offset:src_port_offset+2])[0]
        ports.append(src_port)
    else:
        print(f"Paquet {i}: port source hors limites")

print(f"Nombre de ports extraits: {len(ports)}")
print(f"Premiers ports: {ports[:10]}")

# Compter les fréquences
from collections import Counter
freq = Counter(ports)
print(f"Nombre de ports uniques: {len(freq)}")

# Trouver les singletons (fréquence = 1)
singletons = [p for p, c in freq.items() if c == 1]
print(f"Nombre de singletons: {len(singletons)}")
print(f"Singletons (triés par valeur): {sorted(singletons)[:20]}")

# Trouver les ports fréquents
frequent = [p for p, c in freq.items() if c > 1]
print(f"Ports fréquents: {len(frequent)}")
print(f"Exemples de ports fréquents: {frequent[:10]}")
for p in frequent[:5]:
    print(f"  Port {p}: {freq[p]} occurrences")