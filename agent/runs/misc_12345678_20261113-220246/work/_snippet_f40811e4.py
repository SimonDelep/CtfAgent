import base64

# Tester le décodage de qsTDRC
s = b'qsTDRC'
print(f"Chaîne: {s}")
print(f"Longueur: {len(s)}")

# Base64 nécessite que la longueur soit multiple de 4
# qsTDRC a 6 caractères, donc on peut ajouter 2 '=' pour faire 8
# Mais en réalité, Base64 encode 3 octets en 4 caractères
# 6 caractères Base64 = 6 * 6 = 36 bits = 4.5 octets... ce n'est pas standard

# Essayons de décoder avec padding
try:
    # Ajouter padding si nécessaire
    padded = s + b'=' * (4 - len(s) % 4) if len(s) % 4 != 0 else s
    print(f"Avec padding: {padded}")
    decoded = base64.b64decode(padded)
    print(f"Décodé: {decoded} (hex: {decoded.hex()})")
except Exception as e:
    print(f"Erreur: {e}")

# En fait, qsTDRC a 6 caractères. 6 % 4 = 2, donc on devrait ajouter 2 '='
# Mais 6 caractères Base64 devraient encoder 4.5 octets, ce qui est étrange
# Peut-être que c'est une partie d'une chaîne plus longue

# Vérifions si qsTDRC est suivi par autre chose
with open('audio.wav', 'rb') as f:
    data = f.read()

idx = data.find(b'qsTDRC')
print(f"\nPosition de qsTDRC: {idx}")
print(f"Contexte complet: {data[idx:idx+30]}")