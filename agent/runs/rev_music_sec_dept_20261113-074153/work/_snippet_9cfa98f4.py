import zlib

# Lire le binaire
with open('csirac.pd_linux', 'rb') as f:
    data = f.read()

offset = 0xec31

# Essayer de trouver la fin du flux zlib en testant différentes longueurs
for length in range(1000, len(data)-offset, 1000):
    try:
        decompressor = zlib.decompressobj()
        result = decompressor.decompress(data[offset:offset+length])
        if decompressor.eof:
            print(f"Flux complet trouvé avec length={length}")
            print(f"Taille décompressée: {len(result)}")
            print(f"Premiers octets: {result[:100]}")
            with open('extracted.sf2', 'wb') as sf2:
                sf2.write(result)
            print("Fichier extracted.sf2 sauvegardé")
            break
    except Exception as e:
        pass
else:
    print("Aucun flux complet trouvé avec cette approche")
    
# Essayer avec decompress directement
try:
    result = zlib.decompress(data[offset:])
    print(f"Décompression directe réussie!")
    print(f"Taille: {len(result)}")
    print(f"Premiers octets: {result[:100]}")
except Exception as e:
    print(f"Erreur décompression directe: {e}")