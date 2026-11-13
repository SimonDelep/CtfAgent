# Les ports fréquents - 40000 donnent: [115, 104, 52, 100, 111, 119]
# En ASCII: s, h, 4, d, o, w = "sh4dow"

frequent_ports = [40115, 40104, 40052, 40100, 40111, 40119]
key_from_freq = [p - 40000 for p in frequent_ports]
print("Clé dérivée des ports fréquents:", key_from_freq)
print("En ASCII:", ''.join(chr(k) for k in key_from_freq))

# Maintenant, appliquons cette clé aux singletons
# Mais d'abord, récupérons tous les singletons

# On a besoin de tous les singletons, pas juste les 20 premiers
# Utilisons l'outil pour les obtenir

# Pour l'instant, testons avec les 20 premiers que nous avons
singletons_partial = [50913, 50517, 50915, 50894, 50969, 50581, 50957, 50698, 50142, 50207, 50046, 50573, 50272, 50129, 50784, 50716, 50856, 50695, 50947, 50275]

# Convertissons en mod 256
singletons_mod = [s % 256 for s in singletons_partial]
print("\nSingletons mod 256:", singletons_mod)

# La clé est "sh4dow" = [115, 104, 52, 100, 111, 119]
key = [115, 104, 52, 100, 111, 119]

# XOR avec la clé répétée
def xor_with_key(data, key):
    result = []
    for i, d in enumerate(data):
        result.append(d ^ key[i % len(key)])
    return result

result = xor_with_key(singletons_mod, key)
print("\nRésultat XOR:", result)
print("En ASCII:", ''.join(chr(r) if 32 <= r < 127 else '?' for r in result))
print("En hex:", ''.join(hex(r) for r in result))
