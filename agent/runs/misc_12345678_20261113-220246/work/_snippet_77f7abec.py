import base64
import re

# Lire le fichier audio
with open('audio.wav', 'rb') as f:
    data = f.read()

# Trouver toutes les chaînes Base64 potentielles (caractères A-Za-z0-9+/=, longueur >= 4)
# On cherche des motifs qui ressemblent à du Base64
base64_pattern = re.compile(rb'[A-Za-z0-9+/]{4,}={0,2}')

matches = base64_pattern.findall(data)
print(f"Nombre de chaînes Base64 trouvées: {len(matches)}")

# Tenter de décoder chaque chaîne
decoded_items = []
for i, m in enumerate(matches):
    try:
        decoded = base64.b64decode(m)
        # Vérifier si c'est du texte lisible (ASCII imprimable)
        try:
            text = decoded.decode('ascii')
            if text.isprintable() or all(c.isalnum() or c in '_@{}' for c in text):
                decoded_items.append((i, m.decode('ascii'), text))
        except:
            pass
    except:
        pass

print(f"\nChaînes décodables trouvées: {len(decoded_items)}")
for idx, encoded, decoded in decoded_items:
    print(f"  [{idx}] {encoded} -> {decoded}")

# Afficher les premières chaînes brutes pour voir l'ordre
print("\nPremières chaînes trouvées (brutes):")
for i, m in enumerate(matches[:20]):
    print(f"  [{i}] {m[:50]}...")