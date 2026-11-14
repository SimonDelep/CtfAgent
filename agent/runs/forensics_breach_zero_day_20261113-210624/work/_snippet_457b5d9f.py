import re

with open('fenwick_memdump.txt', 'r', errors='ignore') as f:
    content = f.read()

# Extraire toutes les chaînes imprimables
strings = re.findall(r'[ -~]{8,}', content)

# Chercher des chaînes contenant des mots-clés liés au flag
keywords = ['Service', 'Backdoor', 'Indicator', 'C2', 'WindowsUpdate', 'exe', 'http', 'https', '10.14', 'fenwick']
found = {}

for s in strings:
    for kw in keywords:
        if kw.lower() in s.lower():
            if kw not in found:
                found[kw] = []
            found[kw].append(s)
            break

for kw, vals in found.items():
    print(f"=== {kw} ===")
    for v in set(vals)[:5]:
        print(repr(v))