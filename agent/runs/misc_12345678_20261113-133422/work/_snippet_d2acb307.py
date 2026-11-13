import wave
import struct

with wave.open('audio.wav', 'rb') as wav:
    data = wav.readframes(wav.getnframes())
    samples = struct.unpack('<' + 'h' * (len(data) // 2), data)
    
    # Séparer les canaux gauche et droit
    left = samples[0::2]
    right = samples[1::2]
    
    print(f"Nombre d'échantillons par canal: {len(left)}")
    
    # Regarder les LSB (bit de poids faible) de chaque échantillon
    lsb_left = [s & 1 for s in left]
    lsb_right = [s & 1 for s in right]
    
    # Convertir en chaîne binaire
    lsb_bits_left = ''.join(map(str, lsb_left))
    lsb_bits_right = ''.join(map(str, lsb_right))
    
    # Essayer de convertir en ASCII (8 bits par caractère)
    def bits_to_ascii(bits):
        result = []
        for i in range(0, len(bits) - 7, 8):
            byte = bits[i:i+8]
            val = int(''.join(map(str, byte)), 2)
            if 32 <= val <= 126:
                result.append(chr(val))
            else:
                result.append('?')
        return ''.join(result)
    
    print("LSB gauche (premier 200 chars):", bits_to_ascii(lsb_bits_left)[:200])
    print("LSB droit (premier 200 chars):", bits_to_ascii(lsb_bits_right)[:200])