# Lire le fichier binaire et analyser la structure
with open('capture.pcap', 'rb') as f:
    data = f.read()

# Magic number
magic = data[0:4]
print(f"Magic: {magic.hex()}")

# En-tête PCAP (24 octets)
# Après l'en-tête global, chaque paquet a:
# - 4 octets: timestamp sec
# - 4 octets: timestamp microsec
# - 4 octets: longueur incluse
# - 4 octets: longueur réelle

# Le magic c4c3b2a1 indique un format en little-endian inversé peut-être

# Cherchons les marqueurs dead beef
idx = 0
count = 0
while True:
    pos = data.find(b'\xde\xad\xbe\xef', idx)
    if pos == -1:
        break
    count += 1
    # Regarder ce qui suit
    print(f"dead beef à {pos}: {data[pos:pos+12].hex()}")
    idx = pos + 1
    if count > 10:
        break