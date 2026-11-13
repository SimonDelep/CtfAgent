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
    
    # Essayons de voir si le signe des valeurs encode quelque chose
    # Positif = 1, Négatif = 0
    sign_left = [1 if v >= 0 else 0 for v in left]
    sign_right = [1 if v >= 0 else 0 for v in right]
    
    def bits_to_string(bits):
        result = []
        for i in range(0, len(bits) - 7, 8):
            byte = 0
            for j in range(8):
                byte = (byte << 1) | bits[i + j]
            if 32 <= byte <= 126:
                result.append(chr(byte))
            else:
                result.append('.')
        return ''.join(result)
    
    print("Signe canal gauche (premiers 200 chars):")
    print(bits_to_string(sign_left)[:200])
    
    print("\nSigne canal droit (premiers 200 chars):")
    print(bits_to_string(sign_right)[:200])
    
    # Essayons aussi la différence de signe
    sign_diff = [1 if (l >= 0) != (r >= 0) else 0 for l, r in zip(left, right)]
    print("\nDifférence de signe (premiers 200 chars):")
    print(bits_to_string(sign_diff)[:200])