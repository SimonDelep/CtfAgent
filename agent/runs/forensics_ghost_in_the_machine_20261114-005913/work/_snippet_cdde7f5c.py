# Examinons les données brutes autour du premier paquet
with open('capture.pcap', 'rb') as f:
    data = f.read()

# Premier deadbeef à position 40
start = 40
print(f"Données autour de position 40:")
for i in range(start-4, start+60):
    print(f"{i:4d}: {data[i]:02x}  {chr(data[i]) if 32 <= data[i] < 127 else '.'}")