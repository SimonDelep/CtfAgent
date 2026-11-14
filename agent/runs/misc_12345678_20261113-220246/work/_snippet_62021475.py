import base64
import re

# Lire le fichier audio
with open('audio.wav', 'rb') as f:
    data = f.read()

# Trouver toutes les chaînes Base64 potentielles
base64_pattern = re.compile(rb'[A-Za-z0-9+/]{4,}={0,2}')
matches = base64_pattern.findall(data)

print(f"Total de chaînes trouvées: {len(matches)}")

# Tenter de décoder chaque chaîne et afficher le résultat binaire
all_decoded = b''
for i, m in enumerate(matches):
    try:
        decoded = base64.b64decode(m)
        all_decoded += decoded
    except:
        pass

print(f"\nLongueur totale des données décodées: {len(all_decoded)} octets")
print(f"Premiers 200 octets (représentation hex):")
print(all_decoded[:200].hex())
print(f"\nContenu brut:")
print(all_decoded[:200])

# Chercher "csaw" ou "flag" dans les données décodées
if b'csaw' in all_decoded.lower():
    print("\n'csaw' trouvé dans les données décodées!")
    idx = all_decoded.lower().find(b'csaw')
    print(f"Contexte: {all_decoded[max(0,idx-10):idx+30]}")