import subprocess
import sys

# Exécuter un script Python avec scapy
script = '''
from scapy.all import rdpcap, ICMP, Raw

packets = rdpcap("capture.pcap")
print(f"Nombre de paquets: {len(packets)}")
if len(packets) > 0:
    print(f"Premier paquet: {packets[0].summary()}")
    if packets[0].haslayer(Raw):
        raw_data = bytes(packets[0][Raw])
        print(f"Raw layer (hex): {raw_data.hex()[:200]}")
        print(f"Raw layer (str): {raw_data[:100]}")
'''

result = subprocess.run([sys.executable, "-c", script], capture_output=True, text=True)
print("STDOUT:", result.stdout)
print("STDERR:", result.stderr)