import base64
import re

with open("12345678 (1).wav", "rb") as f:
    data = f.read()

# Chercher toutes les chaînes imprimables potentielles
# On cherche des séquences de caractères ASCII imprimables d'au moins 4 caractères
printable_pattern = re.compile(rb'[\x20-\x7e]{4,}')
matches = printable_pattern.findall(data)

# Filtrer pour trouver des chaînes qui pourraient être du flag ou du Base64
candidates = []
for m in matches:
    # Essayer de décoder en Base64
    try:
        decoded = base64.b64decode(m)
        if len(decoded) >= 2:
            candidates.append((m, decoded))
    except:
        pass

print("Chaînes Base64 décodables:")
for m, d in candidates:
    print(f"  {m} -> {d}")

# Chercher spécifiquement des patterns de type flag
flag_pattern = re.compile(rb'csaw\{[^}]+\}')
flag_matches = flag_pattern.findall(data)
print(f"\nPatterns de flag trouvés: {flag_matches}")

# Chercher des chaînes contenant des underscores ou des caractères spéciaux typiques de flag
special_pattern = re.compile(rb'[a-zA-Z0-9_@!]{4,}')
special_matches = special_pattern.findall(data)
print(f"\nChaînes avec underscores/caractères spéciaux:")
for m in special_matches[:30]:
    print(f"  {m}")