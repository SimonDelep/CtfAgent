import struct

# Lire le fichier WAV et analyser les chunks
with open('/home/etudiantelambda/Documents/CSAW_LLM_2026-BTN-DLP/CtfAgent/CSAW-Quals/misc/12345678/12345678 (1).wav', 'rb') as f:
    data = f.read()

# Chercher le chunk ID3
id3_pos = data.find(b'ID3')
if id3_pos != -1:
    print(f"ID3 trouvé à la position {id3_pos}")
    # Afficher les 200 octets autour de ID3
    print("Contenu autour de ID3:")
    print(data[id3_pos:id3_pos+200])
    
# Chercher aussi le chunk INFO
info_pos = data.find(b'LIST')
if info_pos != -1:
    print(f"\nLIST trouvé à la position {info_pos}")
    print("Contenu autour de LIST:")
    print(data[info_pos:info_pos+200])

# Chercher ICRC (date de création)
icrd_pos = data.find(b'ICRD')
if icrd_pos != -1:
    print(f"\nICRD trouvé à la position {icrd_pos}")
    print("Contenu autour de ICRD:")
    print(data[icrd_pos:icrd_pos+100])