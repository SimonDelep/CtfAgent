# Le fichier session.bin semble avoir un encodage où 0x81 est un préfixe pour les caractères ASCII
# Regardons les données brutes

with open('csirac/session.bin', 'rb') as f:
    data = f.read()

# Cherchons le motif 0x81 suivi d'un caractère
# Décodons: si on voit 0x81, le byte suivant est un caractère ASCII
decoded = []
i = 0
while i < len(data):
    if data[i] == 0x81:
        if i + 1 < len(data):
            decoded.append(chr(data[i+1]))
            i += 2
        else:
            decoded.append('?')
            i += 1
    else:
        # Autres bytes - peut-être des données binaires
        decoded.append(f'[{data[i]:02x}]')
        i += 1

# Affichons les premiers 500 caractères décodés
print(''.join(decoded[:500]))