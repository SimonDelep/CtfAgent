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

# Extraire les ports sources et timestamps
ports_with_ts = []
for ip_start in ip_starts:
    udp_start = ip_start + 20
    if udp_start + 2 <= len(data):
        src_port = int.from_bytes(data[udp_start:udp_start+2], 'big')
        # Timestamp à ip_start - 10
        ts_pos = ip_start - 10
        if ts_pos >= 0:
            ts = int.from_bytes(data[ts_pos:ts_pos+2], 'big')
            ports_with_ts.append((ts, src_port))

# Trier par timestamp
ports_with_ts.sort(key=lambda x: x[0])
ports_ordered = [p for ts, p in ports_with_ts]

# Trouver les singletons (en gardant l'ordre d'apparition)
from collections import Counter
port_counts = Counter(ports_ordered)
singletons_ordered = [p for p in ports_ordered if port_counts[p] == 1]

print(f"Nombre de singletons: {len(singletons_ordered)}")
print(f"Singletons (ordre d'apparition): {singletons_ordered[:20]}")

# Clé "sh4dow"
key = b'sh4dow'
print(f"Clé: {key}")

# Essayer XOR avec les singletons
# Option 1: XOR des valeurs entières
result1 = []
for i, p in enumerate(singletons_ordered):
    k = key[i % len(key)]
    result1.append(p ^ k)
print(f"\nXOR des valeurs entières (premier résultat): {result1[:20]}")

# Option 2: XOR des bytes bas des singletons
result2 = []
for i, p in enumerate(singletons_ordered):
    k = key[i % len(key)]
    result2.append((p % 256) ^ k)
print(f"\nXOR des bytes bas (premier résultat): {result2[:20]}")

# Option 3: XOR des bytes bas, puis convertir en string
try:
    decoded = bytes(result2).decode('utf-8', errors='replace')
    print(f"Décodé: {decoded}")
except:
    print(f"Décodé (repr): {bytes(result2)}")

# Option 4: Peut-être que les singletons doivent être triés par valeur
singletons_sorted = sorted(singletons_ordered)
result3 = []
for i, p in enumerate(singletons_sorted):
    k = key[i % len(key)]
    result3.append((p % 256) ^ k)
print(f"\nXOR des singletons triés par valeur (premier résultat): {result3[:20]}")
try:
    decoded3 = bytes(result3).decode('utf-8', errors='replace')
    print(f"Décodé: {decoded3}")
except:
    print(f"Décodé (repr): {bytes(result3)}")
