import wave
import struct
from collections import Counter

with wave.open('audio.wav', 'rb') as wav:
    frames = wav.readframes(wav.getnframes())
    samples = struct.unpack('<' + 'h' * (len(frames) // 2), frames)
    right = samples[1::2]
    
    def find_silence_sequences(samples, threshold=100):
        sequences = []
        current_len = 0
        in_silence = False
        for s in samples:
            if abs(s) < threshold:
                if not in_silence:
                    in_silence = True
                    current_len = 1
                else:
                    current_len += 1
            else:
                if in_silence:
                    sequences.append(current_len)
                    in_silence = False
                    current_len = 0
        if in_silence:
            sequences.append(current_len)
        return sequences
    
    seqs = find_silence_sequences(right, 100)
    seqs = seqs[1:]  # Ignorer la première
    
    # Trouver les indices des grandes valeurs (>=50)
    large_indices = [i for i, s in enumerate(seqs) if s >= 50]
    print(f"Indices des valeurs >= 50: {large_indices[:20]}")
    print(f"Valeurs correspondantes: {[seqs[i] for i in large_indices[:20]]}")
    
    # Regarder le contexte autour de ces grandes valeurs
    for idx in large_indices[:5]:
        start = max(0, idx - 5)
        end = min(len(seqs), idx + 6)
        print(f"\nAutour de l'index {idx} (valeur {seqs[idx]}):")
        print(f"  Contexte: {seqs[start:end]}")