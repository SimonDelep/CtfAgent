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
    seqs = seqs[1:]
    
    # Identifier les séparateurs (valeurs >= 50)
    groups = []
    current_group = []
    for s in seqs:
        if s >= 50:
            if current_group:
                groups.append(current_group)
                current_group = []
        else:
            current_group.append(s)
    if current_group:
        groups.append(current_group)
    
    # Pour chaque groupe, extraire les valeurs non-1 et voir la structure
    print("Analyse de la structure des groupes:")
    for i, g in enumerate(groups[:5]):
        # Extraire les valeurs non-1
        non_ones = [v for v in g if v != 1]
        print(f"Group {i}: len={len(g)}, non-ones={non_ones[:20]}")
    
    # Peut-être que les valeurs 1 sont des séparateurs et les autres sont des éléments
    # Regardons les séquences de valeurs non-1
    print("\nSéquences de valeurs non-1 entre les 1:")
    for i, g in enumerate(groups[:3]):
        # Trouver les séquences de valeurs non-1
        seqs_non_1 = []
        current = []
        for v in g:
            if v != 1:
                current.append(v)
            else:
                if current:
                    seqs_non_1.append(current)
                    current = []
        if current:
            seqs_non_1.append(current)
        print(f"Group {i}: {seqs_non_1[:10]}")