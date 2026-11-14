import base64
import re

# Lire le fichier audio
with open('audio.wav', 'rb') as f:
    data = f.read()

# Extraire toutes les chaînes Base64 potentielles
# Pattern pour Base64: caractères valides suivis de 0-2 '='
b64_pattern = rb'[A-Za-z0-9+/]{4,}={0,2}'
matches = re.findall(b64_pattern, data)

print(f"Nombre de chaînes Base64 trouvées: {len(matches)}")

# Décoder chaque chaîne et afficher les résultats
decoded_parts = []
for i, m in enumerate(matches):
    try:
        # Ajouter padding si nécessaire
        padded = m + b'=' * (4 - len(m) % 4) if len(m) % 4 else m
        decoded = base64.b64decode(padded)
        decoded_parts.append(decoded)
        # Afficher les chaînes qui sont du texte ASCII lisible
        try:
            text = decoded.decode('ascii')
            if text.isprintable() or '\n' in text:
                print(f"Chain {i}: {m.decode('ascii')} -> {repr(text)}")
        except:
            pass
    except Exception as e:
        pass

# Concaténer tout le payload décodé
full_payload = b''.join(decoded_parts)
print(f"\nTaille totale du payload décodé: {len(full_payload)} octets")
print(f"Hex des derniers 50 octets: {full_payload[-50:].hex()}")
print(f"Fin du payload (repr): {repr(full_payload[-50:])}")