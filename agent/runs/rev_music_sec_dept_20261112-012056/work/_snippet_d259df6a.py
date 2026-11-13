with open('csirac/session.bin', 'rb') as f:
    data = f.read()

# Regardons la structure: peut-être que chaque caractère est XORé avec un byte adjacent
# Ou peut-être que c'est une forme d'encodage différent

# Essayons de voir si le flag est XORé avec une clé répétitive
# D'abord, regardons la séquence complète après flag{ jusqu'à s4lt26

start = 134
end = 182
segment = data[start:end]

# Essayons XOR avec différentes clés pour trouver un pattern
# Si le flag commence par quelque chose de connu, on peut déduire la clé

# Le flag devrait commencer par quelque chose après 'flag{'
# Peut-être que c'est 'csaw{...}' ou 'flag{...}'

# Essayons de trouver la clé en supposant que le premier caractère du flag est '_'
# '_' = 0x5f
# Le premier byte non-0x81 est 0x0a
# Si 0x0a XOR key = 0x5f, alors key = 0x0a XOR 0x5f = 0x55

key = 0x0a ^ 0x5f
print(f"Clé supposée (si premier char est '_'): 0x{key:02x}")

# Appliquons cette clé à tout le segment
decoded = []
for i, b in enumerate(segment):
    if b == 0x81:
        decoded.append(0x81)  # Garde le préfixe
    else:
        decoded.append(b ^ key)

print("Décodé avec clé 0x55:")
print(bytes(decoded))

# Essayons aussi avec d'autres hypothèses
# Peut-être que le flag est 'flag{M4ch1n3_K3y!!}' comme suggéré par les notes
# 'M' = 0x4d
# Si le premier byte 0x0a XOR key = 0x4d, alors key = 0x0a XOR 0x4d = 0x47

key2 = 0x0a ^ 0x4d
print(f"\nClé supposée (si premier char est 'M'): 0x{key2:02x}")

decoded2 = []
for i, b in enumerate(segment):
    if b == 0x81:
        decoded2.append(0x81)
    else:
        decoded2.append(b ^ key2)

print("Décodé avec clé 0x47:")
print(bytes(decoded2))