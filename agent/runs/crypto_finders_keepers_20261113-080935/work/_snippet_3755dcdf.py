# Extrayons plus de contexte autour du bloc XMP
import struct

def read_mp4_metadata(mp4_file):
    with open(mp4_file, 'rb') as f:
        data = f.read()
    
    # Chercher le bloc XMP complet
    # XMP commence généralement par "<?xpacket" ou "<x:xmpmeta"
    xpacket_start = data.find(b'<?xpacket')
    if xpacket_start == -1:
        xpacket_start = data.find(b'<x:xmpmeta')
    
    if xpacket_start != -1:
        print(f"Trouvé XMP à la position {xpacket_start}")
        # Afficher jusqu'à la fin du bloc XMP (chercher ?>)
        xpacket_end = data.find(b'?>', xpacket_start)
        if xpacket_end != -1:
            xpacket_end += 2
            xmp_data = data[xpacket_start:xpacket_end]
            print(f"Longueur du bloc XMP: {len(xmp_data)}")
            print(f"Contenu XMP:\n{xmp_data.decode('utf-8', errors='ignore')}")
    
    # Chercher aussi la chaîne chiffrée directement
    # La chaîne chiffrée est : esnp{d0c_@yz@gl_mn0j_pm3z3_g0_o00s}
    # Cherchons "esnp" ou "csaw" dans les données
    esnp_start = data.find(b'esnp')
    if esnp_start != -1:
        print(f"\nTrouvé 'esnp' à la position {esnp_start}")
        print(f"Contexte: {data[esnp_start:esnp_start+100]}")
    
    # Chercher la chaîne complète
    # esnp{d0c_@yz@gl_mn0j_pm3z3_g0_o00s}
    # Cherchons "esnp{"
    esnp_brace = data.find(b'esnp{')
    if esnp_brace != -1:
        print(f"\nTrouvé 'esnp{{' à la position {esnp_brace}")
        # Trouver la fin de la chaîne (chercher '}')
        end_brace = data.find(b'}', esnp_brace)
        if end_brace != -1:
            cipher = data[esnp_brace:end_brace+1]
            print(f"Chaîne chiffrée: {cipher.decode('utf-8', errors='ignore')}")

read_mp4_metadata('finderskeepers.mp4')