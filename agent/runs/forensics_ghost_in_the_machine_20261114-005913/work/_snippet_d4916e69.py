# Analyser la relation entre singletons et ports fréquents
import struct
from collections import Counter

with open('capture.pcap', 'rb') as f:
    data = f.read()

deadbeef = b'\xde\xad\xbe\xef'
positions = []
pos = 0
while True:
    pos = data.find(deadbeef, pos)
    if pos == -1:
        break
    positions.append(pos)
    pos += 1

src_ports = []
for i in range(0, len(positions), 2):
    second_deadbeef = positions[i+1]
    offset_ip = second_deadbeef + 8
    udp_start = offset_ip + 20
    
    if udp_start + 8 <= len(data):
        udp_header = data[udp_start:udp_start+8]
        src_port = int.from_bytes(udp_header[0:2], 'big')
        src_ports.append(src_port)

port_counts = Counter(src_ports)

# Ports fréquents (plus de 1 occurrence)
frequent_ports = [port for port, count in port_counts.items() if count > 1]
singleton_ports = [port for port, count in port_counts.items() if count == 1]

print(f"Ports fréquents: {sorted(frequent_ports)}")
print(f"Nombre de ports fréquents: {len(frequent_ports)}")
print(f"Nombre de singletons: {len(singleton_ports)}")

# Vérifier les valeurs des ports fréquents % 256
print("\nPorts fréquents % 256:")
for port in sorted(frequent_ports):
    print(f"  {port} % 256 = {port % 256} = {chr(port % 256) if 32 <= port % 256 < 127 else '?'}")

# Peut-être que les singletons XOR avec les ports fréquents donnent le flag?
# Ou les singletons sont XORés avec une clé dérivée des ports fréquents

# Clé dérivée des ports fréquents (ordre d'apparition ou trié)
# Les 6 ports les plus fréquents correspondent à "sh4dow"
key_ports = sorted(frequent_ports)[:6]  # Les 6 ports les plus bas
print(f"\n6 ports les plus bas: {key_ports}")
key = bytes([p % 256 for p in key_ports])
print(f"Clé dérivée: {key}")

# Maintenant, essayer de décrypter les singletons
# Peut-être que chaque singleton est XORé avec la clé de manière cyclique
singletons_order = [port for port in src_ports if port_counts[port] == 1]
print(f"\nNombre de singletons dans l'ordre: {len(singletons_order)}")

# Essai: XOR chaque singleton (comme 2 octets) avec la clé répétée
result = []
for port in singletons_order:
    port_bytes = port.to_bytes(2, 'big')
    for j, b in enumerate(port_bytes):
        key_byte = key[j % len(key)]
        result.append(b ^ key_byte)

print(f"Résultat (premiers 50 bytes): {result[:50]}")
try:
    decoded = bytes(result).decode('ascii', errors='replace')
    print(f"Décodé: {decoded}")
except:
    pass

# Essai alternatif: peut-être que le flag est en hex après XOR?
hex_result = bytes(result).hex()
print(f"\nRésultat hex: {hex_result[:100]}")