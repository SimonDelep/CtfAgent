with open('capture.pcap', 'rb') as f:
    data = f.read()

# Trouver toutes les occurrences de "Se" et extraire les 2 caractères suivants
import re

# Chercher le motif Se suivi de 2 octets
pattern = rb'Se(.{2})'
matches = re.findall(pattern, data)

print(f"Nombre de matches: {len(matches)}")
print("Premiers 20 matches:")
for i, m in enumerate(matches[:20]):
    print(f"{i}: {m!r} -> {m.hex()}")

# Concaténer tous les suffixes
all_suffixes = b''.join(matches)
print(f"\nTous les suffixes concaténés ({len(all_suffixes)} octets):")
print(all_suffixes[:100])