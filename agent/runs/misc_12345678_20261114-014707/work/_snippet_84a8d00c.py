import base64
import re

# Lire le fichier WAV
with open('audio.wav', 'rb') as f:
    data = f.read()

# Extraire toutes les chaînes Base64 potentielles
# Pattern pour Base64: [A-Za-z0-9+/]{4,}={0,2}
b64_pattern = re.compile(r'[A-Za-z0-9+/]{4,}={0,2}')
matches = b64_pattern.findall(data.decode('latin-1'))

print(f"Nombre de chaînes Base64 trouvées: {len(matches)}")

# Afficher les premières chaînes
for i, m in enumerate(matches[:20]):
    print(f"{i}: {m}")

# Tenter de décoder chaque chaîne
decoded_strings = []
for m in matches:
    try:
        # Ajouter le padding si nécessaire
        padded = m + '=' * (4 - len(m) % 4) if len(m) % 4 else m
        decoded = base64.b64decode(padded)
        # Vérifier si c'est du texte ASCII imprimable
        if all(32 <= b < 127 for b in decoded):
            decoded_strings.append((m, decoded.decode('ascii')))
        else:
            decoded_strings.append((m, decoded[:20]))
    except:
        pass

print("\nChaînes décodées en texte ASCII:")
for m, d in decoded_strings:
    print(f"  {m} -> {d}")