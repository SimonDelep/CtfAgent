import zlib

# Lire le binaire
with open('csirac.pd_linux', 'rb') as f:
    data = f.read()

offset = 0xec31

# Essayer avec wbits=-15 (raw deflate sans header)
try:
    decompressor = zlib.decompressobj(wbits=-15)
    result = decompressor.decompress(data[offset:])
    print(f"Décompression raw deflate réussie!")
    print(f"Taille décompressée: {len(result)}")
    print(f"Premiers octets: {result[:100]}")
    with open('extracted.sf2', 'wb') as sf2:
        sf2.write(result)
    print("Fichier extracted.sf2 sauvegardé")
except Exception as e:
    print(f"Erreur raw deflate: {e}")

# Essayer avec wbits=15 (zlib standard)
try:
    decompressor = zlib.decompressobj(wbits=15)
    result = decompressor.decompress(data[offset:])
    print(f"Décompression zlib standard réussie!")
    print(f"Taille décompressée: {len(result)}")
    print(f"Premiers octets: {result[:100]}")
except Exception as e:
    print(f"Erreur zlib standard: {e}")