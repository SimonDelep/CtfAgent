with open('capture.pcap', 'rb') as f:
    magic = f.read(4)
    print(f"Magic: {magic.hex()}")
    print(f"Reversed: {magic[::-1].hex()}")
    
    # Essayons de lire l'entête
    f.seek(0)
    header = f.read(24)
    print(f"Header hex: {header.hex()}")
    
    # Le magic 0xa1b2c3c4 est mentionné dans la description de pcap_parser
    # C'est une variante avec c4 au lieu de d4
    import struct
    magic_val = struct.unpack('>I', magic)[0]
    print(f"Magic as int (big endian): {hex(magic_val)}")
    magic_val_le = struct.unpack('<I', magic)[0]
    print(f"Magic as int (little endian): {hex(magic_val_le)}")
