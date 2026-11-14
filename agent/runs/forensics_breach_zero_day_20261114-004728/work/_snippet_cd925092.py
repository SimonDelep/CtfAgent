import re

# Lire le memdump
with open('fenwick_memdump.txt', 'r') as f:
    content = f.read()

# Chercher toutes les chaînes qui ressemblent à des clés ou indicateurs
# Pattern pour des chaînes alphanumériques longues avec =, +, -, /
patterns = [
    r'[A-Za-z0-9+/=_-]{30,}',  # Chaînes longues
    r'PDQ[=:][A-Za-z0-9+/=_-]+',  # Clés PDQ
    r'C2[A-Za-z0-9+/=_-]{10,}',  # Chaînes avec C2
    r'[A-Za-z0-9+/=_-]{20,}C2[A-Za-z0-9+/=_-]{10,}',  # Chaînes contenant C2
]

print("Recherche de chaînes suspectes:")
for pattern in patterns:
    matches = re.findall(pattern, content)
    if matches:
        print(f"\nPattern: {pattern}")
        for m in set(matches)[:5]:
            print(f"  {m}")

# Chercher aussi des patterns spécifiques comme "C2=" ou "C2:"
c2_patterns = re.findall(r'C2[=:][A-Za-z0-9+/=_-]+', content)
if c2_patterns:
    print(f"\nChaînes avec C2=:")
    for m in set(c2_patterns):
        print(f"  {m}")