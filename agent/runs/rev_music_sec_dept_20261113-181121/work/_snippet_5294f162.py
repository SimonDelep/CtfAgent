# Analyser session.bin pour comprendre l'encodage
with open('csirac/session.bin', 'rb') as f:
    data = f.read()

# Chercher les patterns 0x81xx
i = 0
decoded = []
while i < len(data):
    if data[i] == 0x81 and i+1 < len(data):
        # C'est un caractère encodé 0x81xx
        val = data[i+1]
        decoded.append(val)
        i += 2
    else:
        decoded.append(data[i])
        i += 1

# Afficher les premiers caractères décodés
print("Données décodées (premières 200 octets):")
print(bytes(decoded[:200]))
print()
print("Représentation hex:")
print(bytes(decoded[:200]).hex())