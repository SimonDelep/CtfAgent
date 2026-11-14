import base64
import re

# Re-lisons le fichier WAV pour extraire les chaînes Base64
with open('audio.wav', 'rb') as f:
    data = f.read()

# Extraction regex des chaînes Base64
b64_pattern = re.compile(r'[A-Za-z0-9+/]{4,}={0,2}')
matches = b64_pattern.findall(data.decode('latin-1'))

print(f"Nombre de chaînes Base64 trouvées: {len(matches)}")

# Décodage de chaque chaîne
decoded_parts = []
for i, m in enumerate(matches):
    try:
        # Essayer de décoder avec padding correct
        padded = m + '=' * (4 - len(m) % 4) if len(m) % 4 else m
        decoded = base64.b64decode(padded)
        decoded_parts.append(decoded)
        # Afficher si c'est du texte ASCII lisible
        try:
            text = decoded.decode('ascii')
            if text.isprintable():
                print(f"{i}: '{m}' -> '{text}'")
        except:
            pass
    except Exception as e:
        print(f"{i}: '{m}' -> ERREUR: {e}")

# Concaténation complète
full_payload = b''.join(decoded_parts)
print(f"\nTaille totale du payload décodé: {len(full_payload)} octets")
print(f"Hex dump des derniers 50 octets: {full_payload[-50:].hex()}")
print(f"Fin du payload (repr): {repr(full_payload[-50:])}")