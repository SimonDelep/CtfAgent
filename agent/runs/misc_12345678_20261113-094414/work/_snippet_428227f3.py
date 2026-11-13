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
    
    # Regardons les valeurs absolues du canal droit
    abs_right = [abs(v) for v in right]
    
    # Combien de valeurs sont dans la plage ASCII imprimable?
    ascii_right = [(i, v) for i, v in enumerate(abs_right) if 32 <= v <= 126]
    print(f"Valeurs ASCII dans abs(right): {len(ascii_right)}")
    
    # Afficher les premières
    for i, v in ascii_right[:50]:
        print(f"Pos {i}: {v} -> '{chr(v)}'")
    
    # Essayons de voir si on peut extraire un message en prenant seulement les valeurs ASCII
    msg = ''.join(chr(v) for i, v in ascii_right if 32 <= v <= 126)
    print(f"\nMessage potentiel (premiers 200 chars): {msg[:200]}")