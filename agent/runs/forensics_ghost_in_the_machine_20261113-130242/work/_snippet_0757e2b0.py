import struct

# Lire le fichier pcap
with open('capture.pcap', 'rb') as f:
    data = f.read()

# Vérifier le magic number
print(f"Magic bytes: {data[:4].hex()}")
print(f"Taille totale: {len(data)} octets")

# Chercher les marqueurs deadbeef
deadbeef_count = data.count(b'\xde\xad\xbe\xef')
print(f"Nombre de 'deadbeef': {deadbeef_count}")

# Chercher le magic PCAP standard
print(f"Premiers 20 octets: {data[:20].hex()}")
