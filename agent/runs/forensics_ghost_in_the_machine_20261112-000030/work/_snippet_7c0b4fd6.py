with open('capture.pcap', 'rb') as f:
    data = f.read()

# Extraire les 4 octets après chaque "Se"
se_positions = []
pos = 0
while True:
    pos = data.find(b'Se', pos)
    if pos == -1:
        break
    se_positions.append(pos)
    pos += 1

print("Analyse des 4 octets après chaque 'Se':")
print("Idx | Octets après Se (hex) | Octets 1-2 | Octets 3-4")
print("-" * 60)

for i, pos in enumerate(se_positions[:20]):
    after_se = data[pos+2:pos+6]
    octets_1_2 = after_se[:2]
    octets_3_4 = after_se[2:4]
    print(f"{i:3} | {after_se.hex():16} | {octets_1_2.hex():8} | {octets_3_4.hex()}")

# Regardons aussi les octets 3-4 - peut-être que c'est un compteur
print("\n\nOctets 3-4 (peut-être un compteur?):")
for i, pos in enumerate(se_positions[:20]):
    octets_3_4 = data[pos+4:pos+6]
    print(f"{i}: {octets_3_4.hex()}")