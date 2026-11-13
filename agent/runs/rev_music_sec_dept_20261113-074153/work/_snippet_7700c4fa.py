import zlib

# Lire le binaire
with open('csirac.pd_linux', 'rb') as f:
    data = f.read()

# L'offset 0xec30 donne 0x73, le vrai header zlib est à 0xec31
offset = 0xec31
print(f"Données à partir de l'offset: {data[offset:offset+20].hex()}")

# Essayer de décompresser
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