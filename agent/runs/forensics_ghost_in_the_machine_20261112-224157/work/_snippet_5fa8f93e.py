import struct

# Lire le PCAP
with open('capture.pcap', 'rb') as f:
    data = f.read()

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

# État B seulement
etat_b = [pkt for _, pkt in packets if pkt[22] == 113]

# Trouver les positions constantes dans l'État B
constantes = []
for pos in range(len(etat_b[0])):
    vals = set(pkt[pos] for pkt in etat_b)
    if len(vals) == 1:
        constantes.append((pos, list(vals)[0]))

print(f"Positions constantes dans l'État B: {constantes}")

# Peut-être que la clé est une de ces valeurs?
# Ou peut-être que la clé est dans l'État A?

# État A
etat_a = [pkt for _, pkt in packets if pkt[22] == 64]

constantes_a = []
for pos in range(len(etat_a[0])):
    vals = set(pkt[pos] for pkt in etat_a)
    if len(vals) == 1:
        constantes_a.append((pos, list(vals)[0]))

print(f"Positions constantes dans l'État A: {constantes_a}")

# Comparons les constantes entre État A et État B
print("\nComparaison:")
for pos, val_a in constantes_a:
    if pos < len(etat_b[0]):
        val_b = etat_b[0][pos]
        if val_a != val_b:
            print(f"  Position {pos}: A={val_a}, B={val_b}, XOR={val_a ^ val_b}")