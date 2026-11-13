# Cherchons toutes les chaînes de caractères lisibles dans le fichier MP4
with open('finderskeepers.mp4', 'rb') as f:
    data = f.read()

# Extraire les chaînes de caractères imprimables
import re

# Chercher des chaînes d'au moins 4 caractères imprimables
strings = re.findall(b'[\x20-\x7e]{4,}', data)

print("Chaînes trouvées (longueur >= 4):")
for s in strings:
    try:
        decoded = s.decode('utf-8')
        if len(decoded) >= 4:
            print(f"  {decoded}")
    except:
        pass

# Chercher spécifiquement des chaînes contenant "{" ou "}"
brace_strings = re.findall(b'[\x20-\x7e]*[\{\}][\x20-\x7e]*', data)
print("\nChaînes contenant '{' ou '}':")
for s in brace_strings:
    try:
        decoded = s.decode('utf-8')
        print(f"  {decoded}")
    except:
        pass