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
    
    # Trouver les pics (valeurs absolues > seuil)
    threshold = 10000
    peaks_left = [(i, v) for i, v in enumerate(left) if abs(v) > threshold]
    peaks_right = [(i, v) for i, v in enumerate(right) if abs(v) > threshold]
    
    print(f"Pics dans left (> {threshold}): {len(peaks_left)}")
    print(f"Pics dans right (> {threshold}): {len(peaks_right)}")
    
    # Afficher les premiers pics
    print("\nPremiers pics dans left:")
    for i, v in peaks_left[:20]:
        print(f"Pos {i}: {v}")
    
    print("\nPremiers pics dans right:")
    for i, v in peaks_right[:20]:
        print(f"Pos {i}: {v}")
    
    # Peut-être que les positions des pics contiennent un message?
    # Ou les valeurs des pics?
    
    # Essayons de voir si les valeurs des pics forment un message ASCII
    if peaks_left:
        peak_vals_left = [v for i, v in peaks_left]
        # Convertir en ASCII si possible
        ascii_peaks = [chr(abs(v) % 128) if 32 <= abs(v) % 128 <= 126 else '.' for v in peak_vals_left]
        print(f"\nValeurs des pics (mod 128): {''.join(ascii_peaks[:100])}")