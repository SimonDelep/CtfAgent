import struct
from collections import Counter

with open('capture.pcap', 'rb') as f:
    data = f.read()

# Trouver tous les marqueurs dead beef
marker = bytes.fromhex('deadbeef')
positions = []
pos = 0
while True:
    idx = data.find(marker, pos)
    if idx == -1:
        break
    positions.append(idx)
    pos = idx + 1

# Collecter les ports source et after_ping pour tous les paquets
packets_info = []

for i in range(0, len(positions), 2):
    start = positions[i]
    if start + 54 >= len(data):
        break
    
    src_port = struct.unpack('>H', data[start+34:start+36])[0]
    after_ping = data[start+46:start+54]
    
    packets_info.append((i//2, src_port, after_ping))

# Trouver les singletons
port_counts = Counter([p[1] for p in packets_info])
singletons = [(idx, port, after_ping) for idx, port, after_ping in packets_info if port_counts[port] == 1]

# Trier par ordre d'apparition (déjà trié par idx)
singletons_sorted = sorted(singletons, key=lambda x: x[0])

print(f"Nombre de singletons: {len(singletons_sorted)}")

# Extraire les ports singletons dans l'ordre
singleton_ports = [p[1] for p in singletons_sorted]
print(f"\nPorts singletons (dans l'ordre):")
print(singleton_ports[:20])

# Essayer de convertir les ports en ASCII
# Les ports sont autour de 50000, donc peut-être qu'on doit les modulo 256 ou autre
print("\nPorts mod 256:")
print([p % 256 for p in singleton_ports[:20]])

# Essayer de voir si les ports contiennent des caractères ASCII
# Peut-être que le port est une valeur encodée
print("\nPorts en hex:")
print([hex(p) for p in singleton_ports[:20]])

# Regardons la valeur after_ping pour chaque singleton
print("\nAnalyse de after_ping pour les singletons:")
for idx, port, after_ping in singletons_sorted[:10]:
    # Le premier byte de after_ping semble être un compteur
    seq = after_ping[0]
    # Les bytes 2-3 sont 0xf1 0x53 = 0xf153?
    # bytes 4-7 sont autre chose
    print(f"Packet {idx}: port={port}, seq={seq}, after_ping={after_ping.hex()}")