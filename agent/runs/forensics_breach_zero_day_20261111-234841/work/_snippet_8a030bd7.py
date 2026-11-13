import base64
import re

# Lis le fichier memdump
with open('fenwick_memdump.txt', 'r') as f:
    content = f.read()

# Extraire les chaînes qui ressemblent à du Base64 (contenant +, /, - et =)
# Pattern pour du Base64 standard ou URL-safe
b64_pattern = r'[A-Za-z0-9+/=-]{10,}'

matches = re.findall(b64_pattern, content)

print("Chaînes potentielles Base64 trouvées:")
for m in matches:
    print(f"  {m}")
