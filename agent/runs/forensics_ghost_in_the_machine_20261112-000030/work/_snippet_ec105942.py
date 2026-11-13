import struct

def read_pcap(filename):
    with open(filename, 'rb') as f:
        # Lecture du header pcap
        magic = f.read(4)
        if magic == b'\xd4\xc3\xb2\xa1':
            endian = '<'
        elif magic == b'\xa1\xb2\xc3\xd4':
            endian = '>'
        else:
            print(f"Magic: {magic.hex()}")
            return []
        
        # Version mineure, majeure, timezone, timestamp, snaplen, linktype
        version_minor, version_major, thiszone, sigfigs, snaplen, linktype = struct.unpack(endian + 'HHIIII', f.read(20))
        print(f"Link type: {linktype}, snaplen: {snaplen}")
        
        packets = []
        while True:
            header = f.read(16)
            if len(header) < 16:
                break
            ts_sec, ts_usec, incl_len, orig_len = struct.unpack(endian + 'IIII', header)
            data = f.read(incl_len)
            packets.append((ts_sec, ts_usec, data))
    return packets

packets = read_pcap("capture.pcap")
print(f"Total packets: {len(packets)}")
for i, (ts_sec, ts_usec, data) in enumerate(packets[:5]):
    print(f"Pkt {i}: len={len(data)}, first bytes: {data[:30].hex()}")