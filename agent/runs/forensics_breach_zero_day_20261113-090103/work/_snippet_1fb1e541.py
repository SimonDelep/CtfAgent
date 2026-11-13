# Cherchons plus de chaînes dans le memdump
with open('fenwick_memdump.txt', 'r') as f:
    content = f.read()

# Extraire toutes les chaînes imprimables de longueur >= 4
import re
strings = re.findall(r'[\x20-\x7e]{4,}', content)

# Filtrer les chaînes intéressantes
interesting = []
for s in strings:
    if any(kw in s.lower() for kw in ['flag', 'csaw', 'c2', 'backdoor', 'service', 'http', 'https', 'api', 'key', 'secret', 'token', 'bearer', 'auth', 'password', 'pass', 'user', 'admin', 'root', 'shell', 'cmd', 'exe', 'dll', 'svc', 'service', 'update', 'delivery', 'optimization']):
        interesting.append(s)

# Afficher les résultats uniques
seen = set()
for s in interesting:
    if s not in seen:
        seen.add(s)
        print(s)