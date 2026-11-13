# Extrayons les métadonnées XMP du fichier MP4
import struct

def read_mp4_metadata(mp4_file):
    with open(mp4_file, 'rb') as f:
        data = f.read()
    
    # Chercher les blocs XMP
    # XMP est généralement stocké dans les métadonnées du fichier MP4
    # On peut chercher la chaîne "xmp" ou "XMP" dans les données
    
    # Chercher "xmp" ou "XMP" ou "rdf" (XMP utilise RDF)
    xmp_start = data.find(b'xmp')
    if xmp_start == -1:
        xmp_start = data.find(b'XMP')
    if xmp_start == -1:
        xmp_start = data.find(b'rdf')
    
    if xmp_start != -1:
        # Afficher un peu de contexte autour de xmp_start
        print(f"Trouvé 'xmp' à la position {xmp_start}")
        print(f"Contexte: {data[xmp_start-20:xmp_start+200]}")
    
    # Chercher aussi la chaîne chiffrée directement
    # La chaîne chiffrée est : esnp{d0c_@yz@gl_mn0j_pm3z3_g0_o00s}
    # Cherchons "esnp" ou "csaw" dans les données
    esnp_start = data.find(b'esnp')
    if esnp_start != -1:
        print(f"Trouvé 'esnp' à la position {esnp_start}")
        print(f"Contexte: {data[esnp_start:esnp_start+100]}")
    
    csaw_start = data.find(b'csaw')
    if csaw_start != -1:
        print(f"Trouvé 'csaw' à la position {csaw_start}")
        print(f"Contexte: {data[csaw_start:csaw_start+100]}")
    
    # Chercher aussi les caractères spéciaux comme '@'
    at_start = data.find(b'@')
    if at_start != -1:
        print(f"Premier '@' trouvé à la position {at_start}")
        print(f"Contexte: {data[at_start-20:at_start+50]}")

read_mp4_metadata('finderskeepers.mp4')