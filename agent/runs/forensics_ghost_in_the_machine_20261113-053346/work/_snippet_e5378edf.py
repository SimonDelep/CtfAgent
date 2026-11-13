# On a 504 paquets, 112 singletons, 6 ports fréquents
# Les ports fréquents sont: [40115, 40104, 40052, 40100, 40111, 40119]
# Les singletons sont les autres ports sources

# L'indice dit "some are just there to throw off your averages" - peut-être que 
# certains singletons sont aussi du bruit?

# Ou peut-être que le message est encodé dans l'ordre des singletons par rapport aux fréquents?

# Une autre idée: peut-être que les singletons doivent être triés, et que leur 
# position relative donne le message?

# Ou peut-être que le message est dans les différences entre les singletons?

# Essayons de voir si les singletons, quand on les trie, donnent une séquence
# qui XOR avec la clé donne le message

# D'abord, récupérons tous les ports sources du pcap
# On peut le faire avec tshark ou scapy

import subprocess
import re

# Utilisons tshark pour extraire les ports sources
result = subprocess.run(['tshark', '-r', 'capture.pcap', '-T', 'fields', '-e', 'udp.srcport'], 
                       capture_output=True, text=True)
ports = [int(line) for line in result.stdout.strip().split('\n') if line]
print(f"Total ports: {len(ports)}")

# Comptons les occurrences
from collections import Counter
counts = Counter(ports)
print(f"Nombre de ports uniques: {len(counts)}")

# Ports fréquents (>=60 occurrences)
frequent = [p for p, c in counts.items() if c >= 60]
print(f"Ports fréquents: {sorted(frequent)}")

# Singletons (1 occurrence)
singletons = [p for p, c in counts.items() if c == 1]
print(f"Nombre de singletons: {len(singletons)}")
print(f"Singletons (triés): {sorted(singletons)[:20]}...")

# Maintenant, extrayons les singletons dans l'ordre d'apparition
singleton_order = []
seen = set()
for p in ports:
    if counts[p] == 1 and p not in seen:
        singleton_order.append(p)
        seen.add(p)

print(f"\nSingletons dans l'ordre d'apparition (first 20): {singleton_order[:20]}")
print(f"Total singletons dans l'ordre: {len(singleton_order)}")

# La clé mod 256
key_mod256 = [p % 256 for p in [40115, 40104, 40052, 40100, 40111, 40119]]
print(f"\nClé mod 256: {key_mod256}")

# XOR des singletons (mod 256) avec la clé cyclique
singleton_mod256 = [s % 256 for s in singleton_order]
result = bytes([s ^ key_mod256[i % 6] for i, s in enumerate(singleton_mod256)])
print(f"\nXOR result (first 50): {result[:50]}")
print(f"XOR result (hex): {result[:50].hex()}")