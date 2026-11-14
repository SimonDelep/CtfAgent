# Regardons le code de l'outil mh_subsetsum_solver
# Il devrait être dans le dossier des outils
import os
import glob

# Trouver le fichier de l'outil
for root, dirs, files in os.walk('/home/etudiantelambda/Documents/CSAW_LLM_2026-BTN-DLP/CtfAgent/agent/runs/crypto_secret_treaties_20261113-203758/'):
    for f in files:
        if 'mh_subsetsum' in f.lower():
            print(f"Trouvé: {os.path.join(root, f)}")

# Chercher dans le dossier tools
tools_dir = '/home/etudiantelambda/Documents/CSAW_LLM_2026-BTN-DLP/CtfAgent/agent/runs/crypto_secret_treaties_20261113-203758/tools'
if os.path.exists(tools_dir):
    print(f"\nContenu de {tools_dir}:")
    for f in os.listdir(tools_dir):
        print(f"  {f}")