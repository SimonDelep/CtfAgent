import base64
import re

content = open('fenwick_memdump.txt').read()

# Extraire les chaînes qui ressemblent à du Base64 URL-safe (avec =, -, _)
# Chercher des motifs spécifiques autour de "=" ou avec des patterns de base64

# D''abord, trouvons les chaînes après "=" qui semblent être du base64
# Pattern: quelque chose=base64
matches = re.findall(r'([A-Za-z0-9_-]{10,})=', content)
print("Chaînes avant '=':")
for m in matches[:20]:
    print(f"  {m}")

# Cherchons aussi les chaînes qui pourraient être du base64 URL-safe
# avec des caractères spéciaux comme - et _
b64_like = re.findall(r'([A-Za-z0-9_-]{8,}={0,2})', content)
print("\nChaînes ressemblant à base64:")
for b in b64_like[:30]:
    if not b.startswith('7ff6') and not b.startswith('HKEY') and not b.startswith('Current') and not b.startswith('Security') and not b.startswith('Microsoft') and not b.startswith('Windows') and not b.startswith('Program') and not b.startswith('System') and not b.startswith('Local') and not b.startswith('Control') and not b.startswith('Automatic') and not b.startswith('Duplicate') and not b.startswith('Virtual') and not b.startswith('Internet') and not b.startswith('Create') and not b.startswith('OpenProcess') and not b.startswith('Crypt') and not b.startswith('SeDebug') and not b.startswith('SeAssign') and not b.startswith('SeImpersonate') and not b.startswith('NtQuery') and not b.startswith('WriteProcess') and not b.startswith('HttpSend') and not b.startswith('KERNEL') and not b.startswith('RPC_S') and not b.startswith('STATUS') and not b.startswith('BaseNamed') and not b.startswith('settings') and not b.startswith('Ancillary') and not b.startswith('MicRoo') and not b.startswith('Common') and not b.startswith('bcrypt') and not b.startswith('wsa') and not b.startswith('LSASS') and not b.startswith('propsys') and not b.startswith('oleaut') and not b.startswith('shell32') and not b.startswith('MsMpEng') and not b.startswith('MsSense') and not b.startswith('wmiprvse') and not b.startswith('gdi32') and not b.startswith('userenv') and not b.startswith('wintrust') and not b.startswith('shlwapi') and not b.startswith('shcore') and not b.startswith('rpcrt4') and not b.startswith('bcryptprimitives'):
        print(f"  {b}")
