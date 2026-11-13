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
    
    # Regardons les valeurs du canal droit
    print("Valeurs du canal droit (premiers 100):")
    for i in range(100):
        print(f"{i}: {right[i]}")
    
    # Combien de valeurs non-nulles dans right?
    non_zero = [(i, v) for i, v in enumerate(right) if v != 0]
    print(f"\nValeurs non-nulles dans right: {len(non_zero)} sur {len(right)}")
    
    # Afficher les premières valeurs non-nulles
    print("\nPremières valeurs non-nulles:")
    for i, v in non_zero[:30]:
        print(f"Pos {i}: {v}")