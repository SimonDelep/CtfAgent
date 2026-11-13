from scapy.all import rdpcap, DNS, DNSQR, UDP, TCP, Raw, IP
from collections import Counter

pcap_file = "fenwick_capture.pcap"
packets = rdpcap(pcap_file)

print(f"Total packets: {len(packets)}")

# Compter les types de paquets
dns_count = 0
udp_count = 0
tcp_count = 0
http_count = 0

for pkt in packets:
    if UDP in pkt:
        udp_count += 1
        if DNS in pkt:
            dns_count += 1
    if TCP in pkt:
        tcp_count += 1
    if Raw in pkt:
        try:
            data = bytes(pkt[Raw].load)
            if b"HTTP" in data or b"GET" in data or b"POST" in data:
                http_count += 1
        except:
            pass

print(f"UDP: {udp_count}, TCP: {tcp_count}, DNS: {dns_count}, HTTP: {http_count}")

# Extraire les requêtes DNS
dns_queries = []
for pkt in packets:
    if DNS in pkt and pkt[DNS].qr == 0:  # Query
        if DNSQR in pkt:
            qname = pkt[DNSQR].qname.decode() if isinstance(pkt[DNSQR].qname, bytes) else str(pkt[DNSQR].qname)
            dns_queries.append(qname)

print("\nDNS Queries (first 30):")
for q in dns_queries[:30]:
    print(f"  {q}")

# Extraire les destinations IP uniques
ip_dst = Counter()
for pkt in packets:
    if IP in pkt:
        ip_dst[pkt[IP].dst] += 1

print("\nTop 10 destination IPs:")
for ip, count in ip_dst.most_common(10):
    print(f"  {ip}: {count}")

# Extraire les ports
port_counts = Counter()
for pkt in packets:
    if UDP in pkt:
        port_counts[pkt[UDP].dport] += 1
    if TCP in pkt:
        port_counts[pkt[TCP].dport] += 1

print("\nTop 10 destination ports:")
for port, count in port_counts.most_common(10):
    print(f"  {port}: {count}")