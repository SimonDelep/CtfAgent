import re

with open('fenwick_memdump.txt', 'r', errors='ignore') as f:
    content = f.read()

# Extraire toutes les chaînes imprimables de longueur >= 10
strings = re.findall(r'[ -~]{10,}', content)

# Filtrer pour trouver des chaînes intéressantes
interesting = []
for s in strings:
    # Chercher des chaînes contenant C2, PDQ, ou des patterns suspects
    if 'C2' in s or 'PDQ' in s or 'BACKDOOR' in s or 'INDICATOR' in s:
        interesting.append(s)
    # Chercher des chaînes qui ressemblent à des indicateurs (alphanumériques avec - ou _)
    elif re.match(r'^[A-Za-z0-9_-]{15,}$', s.strip()):
        interesting.append(s)

for i in interesting[:50]:
    print(repr(i))