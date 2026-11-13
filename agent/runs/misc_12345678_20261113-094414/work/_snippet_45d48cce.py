import wave
import struct

# Lire le fichier WAV
with wave.open('audio.wav', 'rb') as wf:
    n_channels = wf.getnchannels()
    sampwidth = wf.getsampwidth()
    n_frames = wf.getnframes()
    frames = wf.readframes(n_frames)

if sampwidth == 2 and n_channels == 2:
    samples = struct.unpack('<' + 'h' * (len(frames) // 2), frames)
    left = samples[0::2]
    right = samples[1::2]
    
    # Essayons de convertir les valeurs en ASCII en prenant le modulo 128 ou en divisant
    # Peut-être que les valeurs sont encodées en base64 ou autre
    
    # Regardons si les valeurs absolues divisées par un facteur donnent des ASCII
    # Ou si le LSB contient le message
    
    # Extraction LSB
    lsb_left = [abs(v) & 1 for v in left]
    lsb_right = [abs(v) & 1 for v in right]
    
    # Convertir en bytes
    def bits_to_string(bits):
        result = []
        for i in range(0, len(bits) - 7, 8):
            byte = 0
            for j in range(8):
                byte = (byte << 1) | bits[i + j]
            if 32 <= byte <= 126:
                result.append(chr(byte))
            else:
                result.append('?')
        return ''.join(result)
    
    print("LSB canal gauche (premiers 200 chars):")
    print(bits_to_string(lsb_left)[:200])
    
    print("\nLSB canal droit (premiers 200 chars):")
    print(bits_to_string(lsb_right)[:200])
    
    # Essayons aussi avec les valeurs absolues directement
    print("\nValeurs absolues modulo 128 (premiers 100):")
    mod_vals = [abs(v) % 128 for v in left[:100]]
    print(mod_vals)
    
    # Convertir en chars si dans la plage imprimable
    chars = []
    for v in mod_vals:
        if 32 <= v <= 126:
            chars.append(chr(v))
        else:
            chars.append('.')
    print(''.join(chars))