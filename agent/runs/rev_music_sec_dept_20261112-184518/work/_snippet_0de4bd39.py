import zlib

with open('csirac/session.bin', 'rb') as f:
    data = f.read()

# Les données chiffrées commencent à 0x8c
# Essayons de décompresser avec zlib à partir de différents offsets

# D'abord, regardons si les données à partir de 0x8c sont un flux zlib
cipher_start = 0x8c
cipher_data = data[cipher_start:]

print(f"Longueur des données à partir de 0x8c: {len(cipher_data)}")
print(f"Premiers octets: {cipher_data[:20].hex()}")

# Essayons de décompresser
try:
    decompressed = zlib.decompress(cipher_data)
    print(f"Décompression réussie! Longueur: {len(decompressed)}")
    print(f"Contenu: {decompressed[:200]}")
except Exception as e:
    print(f"Erreur de décompression: {e}")

# Peut-être que le flux zlib commence plus loin
for offset in range(0x8c, 0x100):
    try:
        decompressed = zlib.decompress(data[offset:])
        if len(decompressed) > 10:
            print(f"Offset {offset}: Décompression réussie! {decompressed[:50]}")
            break
    except:
        pass