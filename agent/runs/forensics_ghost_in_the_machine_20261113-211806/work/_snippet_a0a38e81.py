with open('capture.pcap', 'rb') as f:
    data = f.read()

marker = b'\xde\xad\xbe\xef'
count = data.count(marker)
print(f"Nombre d'occurrences de 'dead beef': {count}")

# Taille du fichier
print(f"Taille du fichier: {len(data)} octets")

# En-tête global PCAP (24 octets)
# Si chaque paquet a 2 marqueurs, alors nombre de paquets = count / 2
print(f"Nombre de paquets estimé (count/2): {count // 2}")

# Regardons la structure autour d'un marqueur
idx = data.find(marker)
print(f"\nPremier marqueur à l'offset: {idx}")
print(f"Données autour du premier marqueur (hex):")
print(data[idx:idx+50].hex())