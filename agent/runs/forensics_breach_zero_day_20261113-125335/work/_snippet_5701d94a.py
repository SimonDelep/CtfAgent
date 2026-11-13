import base64
import re

content = open('fenwick_memdump.txt').read()

# Extraire les chaînes qui ressemblent à du Base64 URL-safe
# Pattern: mélange de A-Za-z0-9 avec - et _ et potentiellement = à la fin

# Cherchons spécifiquement les chaînes après "=" dans le fichier
# Format: "PDQ=SXrPVed5HjrAoV-rtyzpnVs+i4K9gVVk9j"
lines = content.split('\n')
b64_strings = []
for line in lines:
    if '=' in line:
        # Trouver les parties après =
        parts = line.split('=')
        if len(parts) > 1:
            # La partie après = pourrait être du base64
            b64_part = parts[1].strip()
            # Nettoyer: enlever les caractères non base64
            b64_clean = re.sub(r'[^A-Za-z0-9_=-]', '', b64_part)
            if len(b64_clean) >= 10:
                b64_strings.append(b64_clean)

print("Chaînes Base64 trouvées après '=':")
for s in b64_strings[:20]:
    print(f"  {s}")

# Essayons de décoder certaines de ces chaînes
print("\nTentative de décodage:")
for s in b64_strings[:10]:
    try:
        # Essayer de décoder comme base64 URL-safe
        # Remplacer - par + et _ par /
        b64_std = s.replace('-', '+').replace('_', '/')
        # Ajouter du padding si nécessaire
        padding = 4 - len(b64_std) % 4
        if padding != 4:
            b64_std += '=' * padding
        decoded = base64.b64decode(b64_std)
        print(f"  {s[:30]}... -> {decoded[:30]}")
    except Exception as e:
        print(f"  {s[:30]}... -> Erreur: {e}")
