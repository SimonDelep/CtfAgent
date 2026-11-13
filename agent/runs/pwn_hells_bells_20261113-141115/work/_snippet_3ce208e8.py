import struct

# Lire le binaire
with open('thermite-charge', 'rb') as f:
    data = bytearray(f.read())

# Trouver l'interpréteur actuel (./ld-2.31.so)
# L'interpréteur est dans le segment PT_INTERP
# On cherche la chaîne "./ld-2.31.so"
interp = b'./ld-2.31.so\x00'
new_interp = b'/lib64/ld-linux-x86-64.so.2\x00'

# Trouver la position de l'interpréteur
pos = data.find(interp)
print(f"Interpréteur trouvé à la position: {pos}")

if pos != -1:
    # Remplacer par le nouveau interpréteur (en gardant la même taille ou en ajustant)
    # Le nouveau est plus long, donc on doit faire attention
    print(f"Ancien: {interp}")
    print(f"Nouveau: {new_interp}")
    print(f"Longueur ancien: {len(interp)}, nouveau: {len(new_interp)}")
    
    # On va juste remplacer les premiers bytes et espérer que ça passe
    # Mais le problème est que le nouveau est plus long...
    # Essayons de trouver un interpréteur plus court ou de patcher différemment
    
    # Alternative: utiliser patchelf via shell
    print("Essayons patchelf...")