import struct

with open('catalog.db-wal', 'rb') as f:
    data = f.read()

page_size = 1024
frame_header_size = 24
header_size = 32

# Extraire toutes les pages
pages = []
offset = header_size
for i in range(39):
    frame_header = data[offset:offset + frame_header_size]
    page_data = data[offset + frame_header_size:offset + frame_header_size + page_size]
    
    # Header de frame: 
    # - page number (4 octets, big-endian)
    # - commit flag (4 octets) si c'est la dernière page d'une transaction
    page_num = struct.unpack('>I', frame_header[0:4])[0]
    
    # Les 20 octets restants du header de frame
    # offset 4-8: size of db in pages (si commit)
    # offset 8-12: salt1
    # offset 12-16: salt2
    # offset 16-20: checksum
    
    pages.append((page_num, page_data))
    offset += frame_size

print(f"Pages extraites: {len(pages)}")
for page_num, page_data in pages[:5]:
    print(f"Page {page_num}: {len(page_data)} octets, premier octets: {page_data[:20].hex()}")