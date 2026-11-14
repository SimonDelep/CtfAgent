import base64
import re

# Lire le fichier binaire
with open('audio.wav', 'rb') as f:
    data = f.read()

# Chercher des chaînes qui ressemblent à du Base64 (caractères A-Za-z0-9+/=)
# On cherche des séquences d'au moins 4 caractères Base64
base64_pattern = re.compile(rb'[A-Za-z0-9+/]{4,}={0,2}')

matches = base64_pattern.findall(data)

print(f"Nombre de chaînes Base64 trouvées: {len(matches)}")

# Tenter de décoder chaque match
decoded_results = []
for i, match in enumerate(matches):
    try:
        decoded = base64.b64decode(match)
        # Vérifier si le résultat est imprimable/utile
        if len(decoded) > 0:
            # Essayer de décoder en string UTF-8
            try:
                decoded_str = decoded.decode('utf-8')
                if decoded_str.isprintable() or '\n' in decoded_str:
                    decoded_results.append((i, match.decode('ascii'), decoded_str))
            except:
                pass
    except Exception as e:
        pass

print(f"\nChaînes décodables trouvées: {len(decoded_results)}")
for idx, encoded, decoded in decoded_results[:20]:
    print(f"  {idx}: {encoded} -> {decoded}")

if len(decoded_results) > 20:
    print(f"  ... et {len(decoded_results) - 20} autres")