import sys
sys.path.insert(0, './scapy_lib')
from scapy.all import *

def parse_tls_records(data):
    records = []
    i = 0
    while i < len(data):
        if i + 5 > len(data):
            break
        content_type = data[i]
        version = data[i+1:i+3]
        length = int.from_bytes(data[i+3:i+5], 'big')
        if i + 5 + length > len(data):
            break
        record_data = data[i+5:i+5+length]
        records.append((content_type, version, length, record_data))
        i += 5 + length
    return records

packets = rdpcap('capture.pcapng')

tcp_stream = []
for p in packets:
    if TCP in p and p.haslayer(Raw):
        if p[TCP].dport == 443 or p[TCP].sport == 443:
            tcp_stream.append(p)

all_data = b''
for p in tcp_stream:
    raw_data = bytes(p[Raw].load)
    all_data += raw_data

records = parse_tls_records(all_data)

# Trouver les enregistrements Application Data (0x17)
app_data_records = [(i, r) for i, r in enumerate(records) if r[0] == 0x17]
print(f"Nombre d'enregistrements Application Data: {len(app_data_records)}")

for idx, (ct, ver, length, data) in app_data_records[:5]:
    print(f"Record {idx}: length={length}, first_bytes={data[:20].hex()}")