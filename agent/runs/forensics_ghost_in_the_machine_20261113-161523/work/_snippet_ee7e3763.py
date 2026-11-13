# Peut-être que les singletons sont le message XORé avec une clé
# Et la clé est basée sur les ports fréquents d'une manière différente

# Essayons de voir si les singletons - 50000 donnent quelque chose
singletons_partial = [50913, 50517, 50915, 50894, 50969, 50581, 50957, 50698, 50142, 50207, 50046, 50573, 50272, 50129, 50784, 50716, 50856, 50695, 50947, 50275]

# Singleton - 50000
offsets = [s - 50000 for s in singletons_partial]
print("Singletons - 50000:", offsets)

# Peut-être que les offsets sont le message XORé avec la clé
# Et la clé est "sh4dow"

key = [115, 104, 52, 100, 111, 119]  # "sh4dow"

def xor_with_key(data, key):
    result = []
    for i, d in enumerate(data):
        result.append(d ^ key[i % len(key)])
    return result

result = xor_with_key(offsets, key)
print("\nOffsets XOR 'sh4dow':", result)
print("En ASCII:", ''.join(chr(r) if 32 <= r < 127 else '?' for r in result))

# Essayons aussi avec les singletons mod 256
singletons_mod = [s % 256 for s in singletons_partial]
result2 = xor_with_key(singletons_mod, key)
print("\nSingletons mod 256 XOR 'sh4dow':", result2)
print("En ASCII:", ''.join(chr(r) if 32 <= r < 127 else '?' for r in result2))

# Peut-être que la clé est différente. Essayons de voir si les ports fréquents
# donnent une clé différente

# Les ports fréquents sont [40115, 40104, 40052, 40100, 40111, 40119]
# Peut-être que la clé est basée sur les ports fréquents mod 256
key_mod = [p % 256 for p in frequent_ports]
print("\nPorts fréquents mod 256:", key_mod)

result3 = xor_with_key(singletons_mod, key_mod)
print("Singletons mod 256 XOR (frequent mod 256):", result3)
print("En ASCII:", ''.join(chr(r) if 32 <= r < 127 else '?' for r in result3))
