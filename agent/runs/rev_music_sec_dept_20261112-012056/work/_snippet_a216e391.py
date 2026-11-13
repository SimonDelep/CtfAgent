with open('csirac/session.bin', 'rb') as f:
    data = f.read()

# Après flag{ (position 133), cherchons le motif
# On voit 0x81 0x0a (newline), puis 0x02 0x00 0x00 0x00 0x36...
# Peut-être que le flag est encodé avec un XOR ou autre

# Regardons la séquence après flag{
start = 134  # après le '{'
print("Bytes après flag{:")
print(data[start:start+100].hex())

# Cherchons la fin du flag - on attend un '}'
# Peut-être que le flag est XORé avec quelque chose
# Essayons de trouver un motif qui pourrait être '}'

# D'abord, voyons si on peut trouver '}' en cherchant 0x81 suivi de '}' (0x7d)
for i in range(len(data)-1):
    if data[i] == 0x81 and data[i+1] == 0x7d:
        print(f"Trouvé '}}' à la position {i}")

# Cherchons aussi '}' sans le 0x81
for i, b in enumerate(data):
    if b == 0x7d:
        print(f"Trouvé '}}' (0x7d) à la position {i}")