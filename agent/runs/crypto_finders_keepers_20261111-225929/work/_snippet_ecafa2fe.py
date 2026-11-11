import re

with open('finderskeepers.mp4', 'rb') as f:
    data = f.read()

# Cherchons des chaînes ASCII plus longues (10+ caractères)
ascii_strings = re.findall(b'[\x20-\x7e]{10,}', data)
print(f"Chaînes ASCII de 10+ caractères ({len(ascii_strings)}):")
for s in ascii_strings:
    print(f"  {s}")