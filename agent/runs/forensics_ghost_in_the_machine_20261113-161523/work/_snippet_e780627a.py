# Ports singletons dans l'ordre d'apparition
singleton_ports = [50913, 50517, 50915, 50894, 50969, 50581, 50957, 50698, 50142, 50207, 50046, 50573, 50272, 50129, 50784, 50716, 50856, 50695, 50947, 50275, 50143, 50548, 50536, 50342, 50694, 50750, 50809, 50282, 50529, 50402, 50904, 50806, 50235, 50725, 50021, 50330, 50692, 50705, 50850, 50167, 50665, 50188, 50037, 50805, 50743, 50587, 50404, 50908, 50135, 50530, 50643, 50319, 50507, 50727, 50032, 50550, 50209, 50274, 50642, 50655, 50237, 50736, 50571, 50468, 50867, 50604, 50447, 50050, 50124, 50457, 50421, 50866, 50763, 50107, 50566, 50315, 50555, 50051, 50941, 50892, 50965, 50439, 50838, 50887, 50770, 50445, 50175, 50678, 50232, 50293, 50156, 50890, 50240, 50496, 50630, 50462, 50466, 50419, 50840, 50004, 50448, 50996, 50951, 50396, 50017, 50688, 50746, 50895, 50355, 50283, 50187, 50351]

key = b'sh4dow'

# Essayer différentes transformations
print("Essai 1: (port - 50000) XOR key[i % 6]")
result = ''.join(chr((p - 50000) ^ key[i % len(key)]) for i, p in enumerate(singleton_ports))
print(result[:60])

print("\nEssai 2: (port % 256) XOR key[i % 6]")
result = ''.join(chr((p % 256) ^ key[i % len(key)]) for i, p in enumerate(singleton_ports))
print(result[:60])

print("\nEssai 3: (port - 50000) XOR key[i % 6], puis filtrer les imprimables")
result = ''.join(chr((p - 50000) ^ key[i % len(key)]) if 32 <= ((p - 50000) ^ key[i % len(key)]) < 127 else '?' for i, p in enumerate(singleton_ports))
print(result[:60])

print("\nEssai 4: Peut-être que le message est dans les 2 derniers octets du port")
# port = 50xxx, donc les 2 derniers octets sont port % 1000
result = ''.join(chr((p % 1000) ^ key[i % len(key)]) if 32 <= ((p % 1000) ^ key[i % len(key)]) < 127 else '?' for i, p in enumerate(singleton_ports))
print(result[:60])

print("\nEssai 5: Peut-être que le message est simplement port - offset, où offset est dérivé de 'sh4dow'")
# sh4dow en ASCII: 115, 104, 52, 100, 111, 119
# Peut-être que l'offset est la somme ou quelque chose
offset = sum(key)  # 115+104+52+100+111+119 = 601
print(f"Offset = {offset}")
result = ''.join(chr(p - offset) if 32 <= p - offset < 127 else '?' for i, p in enumerate(singleton_ports))
print(result[:60])

print("\nEssai 6: Peut-être que le message est XORé avec une clé dérivée de 'sh4dow'")
# Peut-être que la clé est 'sh4dow' mais appliquée différemment
# Ou peut-être que le message est XORé avec 'csaw{' pour trouver la clé
# Si le premier caractère du message est 'c' (99), alors:
# (port[0] - offset) XOR key[0] = 99
# port[0] = 50913, key[0] = 115 ('s')
# (50913 - offset) XOR 115 = 99
# 50913 - offset = 99 XOR 115 = 18
# offset = 50913 - 18 = 50895
offset = 50913 - (99 ^ 115)
print(f"Offset déduit = {offset}")
result = ''.join(chr(p - offset) if 32 <= p - offset < 127 else '?' for i, p in enumerate(singleton_ports))
print(result[:60])