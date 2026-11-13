with open('capture.pcap', 'rb') as f:
    data = f.read(500)
    print("First 500 bytes (hex):")
    print(data[:100].hex())
    print("\nFirst 500 bytes (repr):")
    print(repr(data[:200]))