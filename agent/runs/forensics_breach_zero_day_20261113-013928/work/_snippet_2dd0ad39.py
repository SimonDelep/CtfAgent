# Extraire toutes les chaînes qui ressemblent à des données encodées du memdump
memdump_content = open('fenwick_memdump.txt', 'r').read()

# Chercher des patterns qui ressemblent à des données encodées (mélange de lettres, chiffres, +, -, _)
import re

# Pattern pour trouver des chaînes avec = dedans
patterns = re.findall(r'[A-Za-z0-9+/=_-]{20,}', memdump_content)
for p in patterns:
    print(p)