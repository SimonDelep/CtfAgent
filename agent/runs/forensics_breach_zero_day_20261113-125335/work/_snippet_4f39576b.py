import base64
import re

# Extraire les chaînes qui ressemblent à du Base64 URL-safe
content = open('fenwick_memdump.txt').read()

# Chercher des motifs qui ressemblent à du base64 URL-safe
# Pattern: mélange de A-Za-z0-9 avec - et _
patterns = re.findall(r'([A-Za-z0-9_-]{10,})', content)

print("Chaînes potentielles Base64 URL-safe:")
for p in patterns:
    print(f"  {p}")
