import wave
import struct

# Lire le fichier WAV
with wave.open('audio.wav', 'rb') as wf:
    n_channels = wf.getnchannels()
    sampwidth = wf.getsampwidth()
    framerate = wf.getframerate()
    n_frames = wf.getnframes()
    frames = wf.readframes(n_frames)

if sampwidth == 2 and n_channels == 2:
    samples = struct.unpack('<' + 'h' * (len(frames) // 2), frames)
    left = samples[0::2]
    right = samples[1::2]
    
    # Regardons les valeurs du canal gauche qui sont dans la plage ASCII imprimable (32-126)
    # Mais les valeurs sont trop grandes (10000+), donc peut-être qu'il faut diviser ou prendre un modulo
    
    # Essayons de voir si les valeurs divisées par un facteur donnent des ASCII
    # Ou peut-être que c'est le LSB qui compte
    
    # Regardons les valeurs brutes du canal gauche
    print("Valeurs du canal gauche (premiers 100):")
    for i in range(100):
        print(f"{i}: {left[i]}")
    
    # Vérifions si certaines valeurs correspondent à des ASCII
    ascii_chars = []
    for i, v in enumerate(left):
        if 32 <= v <= 126:
            ascii_chars.append((i, v, chr(v)))
    
    print(f"\nValeurs ASCII trouvées dans left: {len(ascii_chars)}")
    for i, v, c in ascii_chars[:30]:
        print(f"Pos {i}: {v} -> '{c}'")