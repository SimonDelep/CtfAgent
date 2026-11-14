import re

# Lire le memdump
with open('fenwick_memdump.txt', 'r') as f:
    content = f.read()

# Extraire la clé PDQ=...
pdq_match = re.search(r'PDQ=([A-Za-z0-9+/=-]+)', content)
if pdq_match:
    pdq_key = pdq_match.group(0)
    print(f"PDQ key found: {pdq_key}")
else:
    print("PDQ key not found")

# Extraire la chaîne contenant "C2"
c2_matches = re.findall(r'[A-Za-z0-9+/=_-]{20,}C2[A-Za-z0-9+/=_-]{10,}', content)
print(f"\nChaînes contenant 'C2':")
for m in c2_matches[:5]:
    print(f"  {m}")

# Chercher aussi des chaînes avec "C2" plus larges
c2_lines = [line.strip() for line in content.split('\n') if 'C2' in line and len(line) > 20]
print(f"\nLignes contenant 'C2' (longueur > 20):")
for line in c2_lines[:10]:
    print(f"  {line[:100]}...")