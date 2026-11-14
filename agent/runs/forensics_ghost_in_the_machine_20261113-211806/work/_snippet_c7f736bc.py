import struct

# Parser le fichier pcap manuellement
with open('capture.pcap', 'rb') as f:
    data = f.read()

# Magic number custom: c4c3b2a1
magic = data[:4]
print(f"Magic: {magic.hex()}")

# En-tête global PCAP (24 octets standard, mais peut être différent)
# Format standard: magic (4) + version_major (2) + version_minor (2) + thiszone (4) + sigfigs (4) + snaplen (4) + network (4) = 24 octets
# Ici magic est c4c3b2a1, donc on doit trouver la structure

# Essayons de lire l'en-tête après le magic
header = data[4:28]  # 24 octets d'en-tête après magic
print(f"Header après magic: {header.hex()}")

# Cherchons les marqueurs de paquets: dead beef (pour chaque paquet, il y a 2 marqueurs)
# dead beef = de ad be ef
dead_beef = bytes.fromhex('deadbeef')
beef_dead = bytes.fromhex('beefdead')

# Comptons les occurrences
count_dead_beef = data.count(dead_beef)
count_beef_dead = data.count(beef_dead)
print(f"Occurrences de deadbeef: {count_dead_beef}")
print(f"Occurrences de beefdead: {count_beef_dead}")

# 504 paquets = 1008 marqueurs (2 par paquet)
print(f"Nombre attendu de marqueurs: {504 * 2}")