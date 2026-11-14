import base64
import re

# Lire le fichier audio
with open('audio.wav', 'rb') as f:
    data = f.read()

# Extraire toutes les chaînes Base64 possibles
# Une chaîne Base64 typique contient A-Za-z0-9+/= et a une longueur multiple de 4
# On cherche des séquences de longueur >= 4 qui ressemblent à du Base64

# D'abord, trouvons toutes les séquences Base64 potentielles
# On cherche des chaînes de caractères Base64 d'au moins 4 caractères
base64_pattern = re.compile(rb'[A-Za-z0-9+/]{4,}={0,2}')

matches = base64_pattern.findall(data)
print(f"Nombre de chaînes Base64 trouvées: {len(matches)}")

# Filtrer les chaînes qui sont probablement du vrai Base64 (pas trop courtes, pas trop longues)
valid_matches = []
for m in matches:
    if 4 <= len(m) <= 200:  # Longueur raisonnable
        valid_matches.append(m)

print(f"Nombre de chaînes valides (4-200 chars): {len(valid_matches)}")

# Tenter de décoder chaque chaîne
decoded_parts = []
for i, m in enumerate(valid_matches):
    try:
        decoded = base64.b64decode(m)
        decoded_parts.append((i, m, decoded))
        # Afficher quelques exemples
        if i < 10 or i >= len(valid_matches) - 5:
            print(f"#{i}: {m[:50]}... -> {decoded[:50]}")
    except Exception as e:
        pass

# Concaténer tous les décodages
full_decoded = b''.join([d[2] for d in decoded_parts])
print(f"\nLongueur totale décodée: {len(full_decoded)} octets")
print(f"Début: {full_decoded[:100]}")
print(f"Fin: {full_decoded[-100:]}")

# Chercher des patterns de flag
if b'csaw{' in full_decoded:
    start = full_decoded.find(b'csaw{')
    end = full_decoded.find(b'}', start)
    if end > start:
        flag = full_decoded[start:end+1].decode('utf-8', errors='replace')
        print(f"\nFLAG TROUVÉ: {flag}")