# Re-examinons les données
# Les singletons sont les ports qui n'apparaissent qu'une seule fois
# Les fréquents sont ceux qui apparaissent beaucoup de fois

# Peut-être que la clé est basée sur les ports fréquents, mais d'une manière différente
# Essayons de voir si les ports fréquents forment une séquence qui peut être utilisée comme clé

frequent_ports = [40115, 40104, 40052, 40100, 40111, 40119]

# Essayons différentes transformations
print("Ports fréquents:", frequent_ports)

# Peut-être que la clé est la différence entre les ports fréquents et une base
base = 40000
print("Différence avec base 40000:", [p - base for p in frequent_ports])

# Ou peut-être que la clé est basée sur les 2 derniers octets
print("Derniers octets (port & 0xFF):", [p & 0xFF for p in frequent_ports])
print("Avant-derniers octets (port >> 8):", [(p >> 8) & 0xFF for p in frequent_ports])

# Essayons de voir si les singletons XORés avec quelque chose donnent un flag
# Le flag commence par "csaw{" ou "CTF{"

# Si le premier singleton XORé avec la clé donne 'c' (99) ou 'C' (67)
# singleton[0] = 50913
# 50913 mod 256 = 225
# Si 225 XOR key[0] = 99 ('c'), alors key[0] = 225 XOR 99 = 162
# Si 225 XOR key[0] = 67 ('C'), alors key[0] = 225 XOR 67 = 158

print("225 XOR 99 =", 225 ^ 99)  # devrait être la clé si le premier char est 'c'
print("225 XOR 67 =", 225 ^ 67)  # devrait être la clé si le premier char est 'C'

# Regardons les ports fréquents mod 256
print("Frequent mod 256:", [p % 256 for p in frequent_ports])

# 40115 % 256 = 179
# 40104 % 256 = 168
# 40052 % 256 = 116
# 40100 % 256 = 164
# 40111 % 256 = 175
# 40119 % 256 = 183

# Si la clé est [179, 168, 116, 164, 175, 183]
# Et le premier singleton mod 256 = 225
# 225 XOR 179 = 82 = 'R' (pas 'c')

# Peut-être que la clé est différente. Essayons de trouver la clé qui donne "csaw{"
# Si le message commence par "csaw{", alors:
# c = 99, s = 115, a = 97, w = 119, { = 123

# singleton[0] mod 256 = 225
# 225 XOR key[0] = 99 => key[0] = 225 ^ 99 = 162
# singleton[1] mod 256 = 85
# 85 XOR key[1] = 115 => key[1] = 85 ^ 115 = 30
# singleton[2] mod 256 = 227
# 227 XOR key[2] = 97 => key[2] = 227 ^ 97 = 130
# singleton[3] mod 256 = 206
# 206 XOR key[3] = 119 => key[3] = 206 ^ 119 = 145
# singleton[4] mod 256 = 25
# 25 XOR key[4] = 123 => key[4] = 25 ^ 123 = 98

print("\nClé nécessaire pour 'csaw{':")
singletons_mod = [225, 85, 227, 206, 25]
target = [99, 115, 97, 119, 123]  # "csaw{"
key_needed = [s ^ t for s, t in zip(singletons_mod, target)]
print("Clé nécessaire:", key_needed)
print("En hex:", [hex(k) for k in key_needed])

# Comparons avec les ports fréquents mod 256
print("\nPorts fréquents mod 256:", [p % 256 for p in frequent_ports])
