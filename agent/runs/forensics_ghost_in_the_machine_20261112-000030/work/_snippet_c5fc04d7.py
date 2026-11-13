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

# Extraire les octets 3-4 (compteur) et les octets 1-2 (données)
data_by_counter = {i: [] for i in range(16)}

for i, pos in enumerate(se_positions):
    counter = int.from_bytes(data[pos+4:pos+6], 'little')
    data_val = int.from_bytes(data[pos+2:pos+4], 'little')
    data_by_counter[counter].append(data_val)

# Afficher les premières valeurs pour chaque colonne
print("Premières valeurs de chaque colonne (compteur):")
for col in range(16):
    vals = data_by_counter[col]
    print(f"Colonne {col:2d}: {len(vals):3d} valeurs - premières: {[hex(v) for v in vals[:5]]}")

# Peut-être que le message est dans une colonne spécifique?
# Ou peut-être que c'est une combinaison de toutes les colonnes?