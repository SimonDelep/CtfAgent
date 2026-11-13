import wave
import struct

# Ouvrir le fichier WAV
with wave.open('audio.wav', 'rb') as wav:
    n_frames = wav.getnframes()
    frames = wav.readframes(n_frames)
    total_samples = n_frames * 2  # stéréo
    samples = struct.unpack('<' + 'h' * total_samples, frames)
    
    left = samples[0::2]
    right = samples[1::2]
    
    # Extraire LSB de chaque canal
    lsb_left = [s & 1 for s in left]
    lsb_right = [s & 1 for s in right]
    
    # Différence entre canaux
    diff = [abs(l - r) for l, r in zip(left, right)]
    lsb_diff = [d & 1 for d in diff]
    
    # Convertir en bytes (8 bits)
    def bits_to_bytes(bits):
        result = []
        for i in range(0, len(bits) - 7, 8):
            byte = 0
            for j in range(8):
                byte |= bits[i + j] << (7 - j)
            result.append(byte)
        return bytes(result)
    
    # Essayer de trouver "csaw{" ou "{" dans les LSB
    def find_pattern(bits, pattern):
        pattern_bits = []
        for c in pattern:
            for i in range(8):
                pattern_bits.append((ord(c) >> (7 - i)) & 1)
        pattern_bits = tuple(pattern_bits)
        bits_tuple = tuple(bits)
        idx = 0
        found = []
        while True:
            pos = bits_tuple.find(pattern_bits, idx)
            if pos == -1:
                break
            found.append(pos)
            idx = pos + 1
        return found
    
    # Chercher '{' (0x7b = 01111011)
    pattern_bits = tuple([(ord('{') >> (7 - i)) & 1 for i in range(8)])
    print("Recherche de '{' (0x7b = 01111011):")
    print("  LSB gauche:", find_pattern(lsb_left, pattern_bits)[:5])
    print("  LSB droit:", find_pattern(lsb_right, pattern_bits)[:5])
    print("  LSB diff:", find_pattern(lsb_diff, pattern_bits)[:5])
    
    # Afficher quelques octets des LSB pour voir
    print("\nPremiers 100 octets LSB gauche:", bits_to_bytes(lsb_left[:800])[:50])
    print("Premiers 100 octets LSB droit:", bits_to_bytes(lsb_right[:800])[:50])
    print("Premiers 100 octets LSB diff:", bits_to_bytes(lsb_diff[:800])[:50])