import base64
import re

# Lire le fichier audio
with open('audio.wav', 'rb') as f:
    data = f.read()

# Extraire toutes les chaînes qui ressemblent à du Base64
# Pattern: séquence de caractères Base64 d'au moins 4 caractères
pattern = rb'[A-Za-z0-9+/]{4,}={0,2}'
matches = re.findall(pattern, data)

print(f"Nombre de chaînes Base64 trouvées: {len(matches)}")

# Décode chaque chaîne et afficher les résultats
decoded_results = []
for i, m in enumerate(matches):
    try:
        # Essayer de décoder
        decoded = base64.b64decode(m)
        decoded_results.append((m, decoded))
        if len(decoded) < 50:  # Afficher les petites chaînes
            print(f"{i}: {m} -> {decoded} (hex: {decoded.hex()})")
    except Exception as e:
        pass

print(f"\nTotal chaînes décodables: {len(decoded_results)}")

# Concaténer toutes les parties décodées
full_decoded = b''.join([d for _, d in decoded_results])
print(f"\nLongueur totale décodée: {len(full_decoded)} octets")
print(f"Contenu (premier 200 octets): {full_decoded[:200]}")
print(f"Contenu (hex): {full_decoded[:200].hex()}")