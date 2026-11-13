# Essayons de voir si la clé est "sh4dow" mais avec une transformation différente
# Peut-être que les singletons doivent être traités différemment

# D'abord, obtenons tous les singletons avec leur ordre d'apparition
# Utilisons l'outil extract_singletons

# Pour l'instant, essayons différentes transformations

# Peut-être que les singletons sont déjà le message, mais XORé avec une clé
# Et la clé est "sh4dow" mais répétée

# Ou peut-être que la clé est basée sur les ports fréquents d'une manière différente
# Essayons de voir si les ports fréquents forment une clé en utilisant une autre transformation

frequent_ports = [40115, 40104, 40052, 40100, 40111, 40119]

# Essayons de voir si la clé est basée sur les ports fréquents triés par valeur
sorted_freq = sorted(frequent_ports)
print("Ports fréquents triés:", sorted_freq)
print("Triés - 40000:", [p - 40000 for p in sorted_freq])
print("En ASCII:", ''.join(chr(p - 40000) for p in sorted_freq))

# Ou peut-être que la clé est basée sur l'ordre d'apparition des singletons
# et les ports fréquents sont juste pour extraire la clé

# Essayons de voir si le message commence par "csaw{"
# Si le premier singleton XORé avec la clé donne 'c' (99)
# singleton[0] = 50913
# 50913 % 256 = 225
# 225 XOR key[0] = 99 => key[0] = 162

# Mais "sh4dow"[0] = 115 ('s')
# 225 XOR 115 = 146 (pas 'c')

# Peut-être que la clé est différente. Essayons de trouver la clé qui donne "csaw{"
# en utilisant les 5 premiers singletons

singletons_partial = [50913, 50517, 50915, 50894, 50969]
singletons_mod = [s % 256 for s in singletons_partial]
print("\nSingletons mod 256:", singletons_mod)

# Si le message est "csaw{", alors:
target = [99, 115, 97, 119, 123]  # "csaw{"
key_needed = [s ^ t for s, t in zip(singletons_mod, target)]
print("Clé nécessaire pour 'csaw{':", key_needed)
print("En ASCII:", ''.join(chr(k) if 32 <= k < 127 else '?' for k in key_needed))

# Comparons avec "sh4dow"
print("\n' sh4dow' en ASCII:", [ord(c) for c in "sh4dow"])

# Peut-être que la clé est "sh4dow" mais avec une transformation
# Ou peut-être que la clé est basée sur les ports fréquents d'une manière différente

# Essayons de voir si les ports fréquents - 40000 donnent la clé
print("\nPorts fréquents - 40000:", [p - 40000 for p in frequent_ports])

# Peut-être que la clé est l'inverse de "sh4dow"
print("Inversé:", [p - 40000 for p in reversed(frequent_ports)])
