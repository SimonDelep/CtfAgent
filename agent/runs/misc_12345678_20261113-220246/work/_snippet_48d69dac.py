with open('audio.wav', 'rb') as f:
    data = f.read()

# Chunk ID3 à la position 6064294
id3_start = 6064294
id3_header = data[id3_start:id3_start+10]
print(f"En-tête ID3: {id3_header.hex()}")
print(f"  Signature: {id3_header[0:3]}")
print(f"  Version: {id3_header[3:5]}")
print(f"  Flags: {id3_header[5]}")

# Taille en synchsafe integer
size_bytes = id3_header[6:10]
size = (size_bytes[0] << 21) | (size_bytes[1] << 14) | (size_bytes[2] << 7) | size_bytes[3]
print(f"  Taille (synchsafe): {size}")

# Le payload ID3 commence après l'en-tête de 10 octets
id3_payload = data[id3_start+10:id3_start+10+size]
print(f"\nPayload ID3 ({len(id3_payload)} octets):")
print(f"  Hex: {id3_payload[:100].hex()}")
print(f"  Brut: {id3_payload[:100]}")

# Chercher des strings dans le payload
import re
strings = re.findall(rb'[\x20-\x7e]{4,}', id3_payload)
print(f"\nStrings trouvées dans ID3 payload:")
for s in strings:
    print(f"  {s}")

# Essayer de décoder comme Base64
base64_strings = re.findall(rb'[A-Za-z0-9+/]{4,}={0,2}', id3_payload)
print(f"\nChaînes Base64 dans ID3:")
for s in base64_strings:
    try:
        decoded = base64.b64decode(s)
        print(f"  {s} -> {decoded}")
    except:
        print(f"  {s} -> (échec)")