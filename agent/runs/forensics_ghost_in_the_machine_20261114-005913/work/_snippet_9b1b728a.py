with open('capture.pcap', 'rb') as f:
    data = f.read()

# Trouver tous les débuts d'IP
ip_starts = []
for i in range(40, len(data)-40):
    if data[i] == 0x45:
        ihl = data[i] & 0x0F
        version = (data[i] >> 4) & 0x0F
        if version == 4 and ihl == 5:
            if data[i+12] == 0x0a:
                ip_starts.append(i)

# Extraire les ports source et destination
src_ports = []
dst_ports = []
for ip_start in ip_starts:
    udp_start = ip_start + 20
    if udp_start + 4 <= len(data):
        src_port = int.from_bytes(data[udp_start:udp_start+2], 'big')
        dst_port = int.from_bytes(data[udp_start+2:udp_start+4], 'big')
        src_ports.append(src_port)
        dst_ports.append(dst_port)

print(f"Ports source uniques: {len(set(src_ports))}")
print(f"Ports destination uniques: {len(set(dst_ports))}")
print(f"Ports destination: {set(dst_ports)}")

# Vérifier les métadonnées (4 octets après le deuxième deadbeef)
# deadbeef à positions[i] et positions[i+1]
# IP à positions[i+1] + 8
# Métadonnées à positions[i+1] + 4 à positions[i+1] + 8

# Trouver les positions des deadbeef
deadbeef = b'\xde\xad\xbe\xef'
positions = []
pos = 0
while True:
    idx = data.find(deadbeef, pos)
    if idx == -1:
        break
    positions.append(idx)
    pos = idx + 1

print(f"\nNombre de deadbeef: {len(positions)}")

# Extraire les métadonnées pour chaque paquet
# Chaque paquet a 2 deadbeef, donc positions[2*i] et positions[2*i+1]
metadata = []
for i in range(0, len(positions)-1, 2):
    second_deadbeef = positions[i+1]
    # Métadonnées à second_deadbeef + 4 à second_deadbeef + 8
    if second_deadbeef + 8 <= len(data):
        meta = data[second_deadbeef+4:second_deadbeef+8]
        metadata.append(meta)

print(f"Nombre de métadonnées: {len(metadata)}")
print(f"Premières métadonnées: {metadata[:10]}")

# Convertir en entier
meta_ints = [int.from_bytes(m, 'big') for m in metadata]
print(f"Premières métadonnées (int): {meta_ints[:10]}")

# Vérifier si les métadonnées contiennent la clé
from collections import Counter
meta_counts = Counter(meta_ints)
print(f"\nMétadonnées fréquentes: {meta_counts.most_common(10)}")
