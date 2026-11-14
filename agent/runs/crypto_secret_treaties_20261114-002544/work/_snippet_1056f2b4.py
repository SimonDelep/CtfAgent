# Charger les données
pubkey = []
with open('pubkey.txt', 'r') as f:
    for line in f:
        line = line.strip()
        if line and not line.startswith('#'):
            pubkey.append(int(line))

ciphertexts = []
with open('ciphertext.txt', 'r') as f:
    for line in f:
        line = line.strip()
        if line and not line.startswith('#'):
            ciphertexts.append(int(line))

# L'outil mh_subsetsum_lll est actif, essayons de l'appeler
# Il devrait être importable depuis somewhere
# Vérifions d'abord ce qui est disponible

import sys
print("Modules disponibles:")
for mod in sorted(sys.modules.keys()):
    if 'mh' in mod.lower() or 'forge' in mod.lower():
        print(f"  {mod}")

# Essayons d'importer directement
try:
    from mh_subsetsum_lll import main
    print("Importé mh_subsetsum_lll.main")
except Exception as e:
    print(f"Erreur import: {e}")

# Peut-être que l'outil est enregistré dans un module spécial
# Cherchons dans sys.modules
for mod_name, mod in sys.modules.items():
    if hasattr(mod, 'main') and 'mh' in mod_name.lower():
        print(f"Trouvé main dans {mod_name}")