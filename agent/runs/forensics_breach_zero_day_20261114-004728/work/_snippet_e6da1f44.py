with open('fenwick_memdump.txt', 'r', errors='ignore') as f:
    content = f.read()

# Chercher PDQ=
import re
matches = re.findall(r'PDQ=[A-Za-z0-9+/=-]+', content)
print("Matches PDQ=:", matches)

# Chercher aussi la chaîne avec C2
matches_c2 = re.findall(r'[A-Za-z0-9+/=_-]{20,}', content)
c2_matches = [m for m in matches_c2 if 'C2' in m]
print("Chaînes avec C2:", c2_matches[:5])