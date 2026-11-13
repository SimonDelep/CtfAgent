with open('capture.pcap', 'rb') as f:
    data = f.read(100)
    print("First 100 bytes hex:")
    for i in range(0, len(data), 16):
        hex_part = ' '.join(f'{b:02x}' for b in data[i:i+16])
        ascii_part = ''.join(chr(b) if 32 <= b < 127 else '.' for b in data[i:i+16])
        print(f"{i:04x}: {hex_part:<48} {ascii_part}")
