# Analyser plus en détail le code pour trouver la logique de déchiffrement
# On voit des références à des adresses relatives

with open('nitro', 'rb') as f:
    data = f.read()

# Chercher les références à enccode (0x40130d)
# Dans le code, les références relatives sont encodées différemment

# Regardons la fonction à 0x11d0 qui semble être main()
# Elle contient des appels et manipulations de mémoire

# Chercher "Access denied" qui est dans .rodata à 0x2050
# Cela nous aidera à trouver la fonction secret_check

# D'abord, trouvons où est appelée la fonction qui affiche "Access denied"
# Le message est à 0x2050 dans le fichier (offset)

# Regardons les appels dans le code
# À 0x11f0, on voit: 48 8d 0d 85 0e 00 00 -> lea rdx, [rip + 0xe85]
# rip est après l'instruction (7 bytes), donc adresse = rip + 0xe85

# Calculons: 0x11f0 + 7 + 0xe85 = 0x11f7 + 0xe85 = 0x207c
# 0x207c - 0x2000 = 0x7c -> c'est dans .rodata

# Cherchons la fonction qui compare le mot de passe
# On voit à 0x1270: ba 07 00 00 00 -> mov edx, 7 (longueur?)
# Puis un appel à 0x1277 + 7 + 0xfe3a = ...

# Essayons de désassembler manuellement la fonction principale
print("=== Analyse de la fonction à 0x11d0 (probablement main) ===")
func_start = 0x11d0
func_code = data[func_start:func_start+200]

# Afficher avec décalages relatifs
for i in range(0, len(func_code), 16):
    hex_part = ' '.join(f'{b:02x}' for b in func_code[i:i+16])
    print(f"{func_start + i:08x}: {hex_part}")

# Chercher les appels (e8 xx xx xx xx)
print("\n=== Recherche d'appels (e8) ===")
offset = 0
while offset < len(func_code) - 4:
    if func_code[offset] == 0xe8:
        # Appel relatif
        rel_addr = int.from_bytes(func_code[offset+1:offset+5], 'little', signed=True)
        target = (func_start + offset + 5) + rel_addr
        print(f"Appel à 0x{target:x} (relatif {rel_addr:+d}) à offset {func_start + offset:x}")
    offset += 1