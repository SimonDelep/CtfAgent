# Ports bruit
noise_ports = [40052, 40100, 40104, 40111, 40115, 40119]

print("Ports bruit:")
for p in noise_ports:
    print(f"  {p} = {bin(p)}")

# Différences
print("\nDifférences entre ports bruit:")
for i in range(len(noise_ports)):
    for j in range(i+1, len(noise_ports)):
        diff = noise_ports[j] - noise_ports[i]
        print(f"  {noise_ports[j]} - {noise_ports[i]} = {diff}")

# Peut-être que ces ports représentent des colonnes
# 6 ports = 6 colonnes ? Mais le hint mentionne 16 colonnes...

# Regardons les ports signal - peut-être qu'ils contiennent des indices
signal_ports = [50004, 50017, 50021, 50032, 50037, 50046, 50050, 50051, 50107, 50124, 50129, 50135, 50142, 50143, 50156, 50167, 50175, 50187, 50188, 50207, 50209, 50232, 50235, 50237, 50240, 50272, 50274, 50275, 50282, 50283, 50293, 50315, 50319, 50330, 50342, 50351, 50355, 50396, 50402, 50404, 50419, 50421, 50439, 50445, 50447, 50448, 50457, 50462, 50466, 50468, 50496, 50507, 50517, 50529, 50530, 50536, 50548, 50550, 50555, 50566, 50571, 50573, 50581, 50587, 50604, 50608, 50630, 50631, 50642, 50643, 50655, 50665, 50678, 50688, 50692, 50694, 50695, 50698, 50705, 50716, 50725, 50727, 50736, 50743, 50746, 50750, 50763, 50770, 50784, 50805, 50806, 50809, 50838, 50840, 50850, 50856, 50866, 50867, 50887, 50890, 50892, 50894, 50895, 50904, 50908, 50913, 50915, 50941, 50947, 50951, 50957, 50965, 50969, 50972, 50996]

print(f"\nNombre de ports signal uniques: {len(set(signal_ports))}")

# Peut-être que les ports signal sont des valeurs XORées avec une clé
# Essayons de voir si les ports signal modulo quelque chose donne un motif
print("\nPorts signal modulo 16:")
mods = [p % 16 for p in signal_ports]
from collections import Counter
print(Counter(mods))