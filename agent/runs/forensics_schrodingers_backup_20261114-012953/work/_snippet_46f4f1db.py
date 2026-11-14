import struct

with open('catalog.db-wal', 'rb') as f:
    data = f.read()

page_size = 1024

# Regarder la frame 0 en détail
offset = 32
page_num = struct.unpack('>I', data[offset:offset+4])[0]
commit_flag = struct.unpack('>I', data[offset+4:offset+8])[0]
page_data = data[offset+8:offset+8+page_size]

print(f"Frame 0: page={page_num}, commit={commit_flag}")
print(f"Octets 991-1023: {page_data[991:1023].hex()}")
print(f"Premiers 4 octets: {page_data[991:995].hex()}")
print(f"Valeur attendue: 23010300")
print(f"Match: {page_data[991:995] == b'\\x23\\x01\\x03\\x00'}")

# Vérifier la valeur exacte
print(f"Bytes: {[hex(b) for b in page_data[991:995]]}")