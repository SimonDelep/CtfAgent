import sys
import subprocess

# Vérifier où scapy est installé
result = subprocess.run(['pip', 'show', 'scapy'], capture_output=True, text=True)
print("pip show scapy:")
print(result.stdout)
print(result.stderr)

# Essayer d'importer avec le bon chemin
import importlib.util
spec = importlib.util.find_spec("scapy")
print(f"Spec trouvé: {spec}")