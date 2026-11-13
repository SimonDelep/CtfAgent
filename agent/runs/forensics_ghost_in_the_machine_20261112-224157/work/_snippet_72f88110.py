with open('capture.pcap', 'rb') as f:
    data = f.read()

print(f"Total size: {len(data)} bytes")

# Cherchons la structure des paquets
# Le fichier semble avoir un header global puis des paquets
# Regardons les premiers octets
magic = data[:4]
print(f"Magic: {magic.hex()}")

# Cherchons les occurrences de "PING"
ping_positions = []
pos = 0
while True:
    pos = data.find(b'PING', pos)
    if pos == -1:
        break
    ping_positions.append(pos)
    pos += 1

print(f"Nombre d'occurrences de 'PING': {len(ping_positions)}")
print(f"Positions des 10 premiers PING: {ping_positions[:10]}")

# Regardons ce qui précède chaque PING
for i, pos in enumerate(ping_positions[:5]):
    print(f"\n--- PING #{i+1} à offset {pos} ---")
    print(f"Contexte avant: {data[pos-20:pos].hex()}")
    print(f"Contexte après: {data[pos+4:pos+24].hex()}")