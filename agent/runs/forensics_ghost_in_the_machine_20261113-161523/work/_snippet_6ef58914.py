# Ports singletons et fréquents extraits
singletons = [50913, 50517, 50915, 50894, 50969, 50581, 50957, 50698, 50142, 50207, 50046, 50573, 50272, 50129, 50784, 50716, 50856, 50695, 50947, 50275]
frequent = [40115, 40104, 40052, 40100, 40111, 40119]

# Essayons différentes approches
print("Singletons mod 256:", [s % 256 for s in singletons[:10]])
print("Frequent mod 256:", [f % 256 for f in frequent])

# Peut-être que la clé est basée sur l'offset par rapport à une base
base = 50000
print("Singletons - base:", [s - base for s in singletons[:10]])

# Ou peut-être que les singletons sont déjà le message XORé avec une clé
# Et la clé est dans les ports fréquents d'une manière différente
# Essayons de voir si les ports fréquents forment un mot
print("Frequent as chars (mod 256):", ''.join(chr(f % 256) for f in frequent))

# Peut-être que la clé est répétée et on doit XORer
key_mod = [f % 256 for f in frequent]
print("Key mod 256:", key_mod)

# Si on XOR les singletons avec la clé répétée
def xor_with_key(data, key):
    result = []
    for i, d in enumerate(data):
        result.append(d ^ key[i % len(key)])
    return result

# Test avec les 20 premiers singletons
key = [f % 256 for f in frequent]
result = xor_with_key([s % 256 for s in singletons[:20]], key)
print("XOR result:", result)
print("As chars:", ''.join(chr(r) if 32 <= r < 127 else '?' for r in result))
