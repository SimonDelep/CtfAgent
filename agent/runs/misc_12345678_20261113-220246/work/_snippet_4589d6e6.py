import base64
import re

# Lire le fichier audio
with open('audio.wav', 'rb') as f:
    data = f.read()

# Trouver toutes les séquences Base64 avec leur position
base64_pattern = rb'[A-Za-z0-9+/]{4,}={0,2}'
matches = list(re.finditer(base64_pattern, data))

print(f"Nombre de matches: {len(matches)}")

# Trier par position et décoder dans l'ordre
decoded_parts = []
for m in matches:
    seq = m.group()
    pos = m.start()
    try:
        # Ajouter padding si nécessaire
        padded = seq + b'=' * ((4 - len(seq) % 4) % 4)
        decoded = base64.b64decode(padded)
        decoded_parts.append((pos, seq, decoded))
    except Exception as e:
        print(f"Erreur à pos {pos}: {seq} -> {e}")

# Afficher les parties décodées dans l'ordre
print("\nParties décodées dans l'ordre:")
for pos, seq, decoded in decoded_parts:
    if len(decoded) < 20:
        print(f"pos={pos}: {seq} -> {decoded} (hex: {decoded.hex()})")
    else:
        print(f"pos={pos}: {seq} -> [{len(decoded)} octets]")

# Concaténer dans l'ordre
full_decoded = b''.join([d for _, _, d in decoded_parts])
print(f"\nLongueur totale: {len(full_decoded)} octets")
print(f"Contenu: {full_decoded}")
print(f"Hex: {full_decoded.hex()}")