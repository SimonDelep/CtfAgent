# Lisons le fichier et cherchons des patterns
with open('finderskeepers.mp4', 'rb') as f:
    data = f.read()

print(f"Taille: {len(data)} bytes")
print(f"Premiers 100 bytes (hex): {data[:100].hex()}")
print(f"Premiers 100 bytes (repr): {repr(data[:100])}")

# Cherchons des chaînes ASCII imprimables
import re
ascii_strings = re.findall(b'[\x20-\x7e]{4,}', data)
print(f"\nChaînes ASCII trouvées ({len(ascii_strings)}):")
for s in ascii_strings[:20]:
    print(f"  {s}")