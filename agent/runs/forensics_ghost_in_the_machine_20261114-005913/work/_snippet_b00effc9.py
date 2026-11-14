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

# Option: ((singleton - 50000) % 256) XOR key
result = []
for i, p in enumerate(singletons_ordered):
    adjusted = (p - 50000) % 256
    k = key[i % len(key)]
    result.append(adjusted ^ k)

print(f"\nRésultat (premier): {result[:30]}")
try:
    decoded = bytes(result).decode('utf-8', errors='replace')
    print(f"Décodé: {decoded}")
except Exception as e:
    print(f"Erreur: {e}")
    print(f"Bytes: {bytes(result)}")

# Essayer aussi avec les singletons triés par valeur
singletons_sorted = sorted(singletons_ordered)
result2 = []
for i, p in enumerate(singletons_sorted):
    adjusted = (p - 50000) % 256
    k = key[i % len(key)]
    result2.append(adjusted ^ k)

print(f"\nRésultat trié par valeur (premier): {result2[:30]}")
try:
    decoded2 = bytes(result2).decode('utf-8', errors='replace')
    print(f"Décodé: {decoded2}")
except Exception as e:
    print(f"Erreur: {e}")
    print(f"Bytes: {bytes(result2)}")
