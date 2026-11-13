import zlib

# Lire le binaire
with open('csirac.pd_linux', 'rb') as f:
    data = f.read()

# Offset identifié : 0xec30
offset = 0xec30
print(f"Taille du fichier: {len(data)}")
print(f"Offset de début: {offset} (0x{offset:x})")
print(f"Données à partir de l'offset: {data[offset:offset+20].hex()}")

# Essayer de décompresser à partir de cet offset
try:
    decompressor = zlib.decompressobj()
    result = decompressor.decompress(data[offset:])
    print(f"Décompression réussie!")
    print(f"Taille décompressée: {len(result)}")
    print(f"Premiers octets: {result[:100]}")
    # Sauvegarder le SF2
    with open('extracted.sf2', 'wb') as sf2:
        sf2.write(result)
    print("Fichier extracted.sf2 sauvegardé")
except Exception as e:
    print(f"Erreur: {e}")
    # Essayer avec différents offsets
    for test_offset in range(offset-5, offset+5):
        try:
            decompressor = zlib.decompressobj()
            result = decompressor.decompress(data[test_offset:])
            print(f"Offset {test_offset} (0x{test_offset:x}) fonctionne!")
            print(f"Premiers octets: {result[:50]}")
            break
        except:
            pass