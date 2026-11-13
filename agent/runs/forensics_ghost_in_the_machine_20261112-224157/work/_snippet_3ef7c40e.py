import struct

# Lire le fichier pcap
with open('capture_fixed.pcap', 'rb') as f:
    data = f.read()

print(f"Taille totale: {len(data)} octets")

# Header PCAP (24 octets)
magic = struct.unpack('<I', data[0:4])[0]
print(f"Magic bytes: {hex(magic)}")

# Vérifier la structure
# Header global PCAP = 24 octets
# Ensuite, chaque paquet a un header de 16 octets + données

# Essayons de parser comme un fichier PCAP standard
offset = 24  # Après le header global
packet_count = 0

while offset < len(data):
    if offset + 16 > len(data):
        break
    
    # Header de paquet PCAP: ts_sec(4), ts_usec(4), incl_len(4), orig_len(4)
    ts_sec, ts_usec, incl_len, orig_len = struct.unpack('<IIII', data[offset:offset+16])
    
    if incl_len == 0 or incl_len > 1000:  # Valeur suspecte
        break
    
    packet_data = data[offset+16:offset+16+incl_len]
    
    if packet_count < 5:
        print(f"Paquet {packet_count}: ts={ts_sec}.{ts_usec}, incl_len={incl_len}, orig_len={orig_len}")
        print(f"  Données (hex): {packet_data[:40].hex()}")
    
    offset += 16 + incl_len
    packet_count += 1

print(f"\nTotal paquets parsés: {packet_count}")
print(f"Offset final: {offset}, taille fichier: {len(data)}")