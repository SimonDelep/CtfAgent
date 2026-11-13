from scapy.all import rdpcap, TCP, IP, Raw

packets = rdpcap('capture.pcap')

# Afficher les ports et adresses IP uniques
ips = set()
ports = set()
for pkt in packets:
    if IP in pkt:
        ips.add(pkt[IP].src)
        ips.add(pkt[IP].dst)
    if TCP in pkt:
        ports.add(pkt[TCP].sport)
        ports.add(pkt[TCP].dport)

print("IPs:", sorted(ips))
print("Ports:", sorted(ports))
print("Nombre de paquets:", len(packets))