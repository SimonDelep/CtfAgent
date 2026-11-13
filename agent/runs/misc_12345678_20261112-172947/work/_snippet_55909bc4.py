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
    
    # Identifier les séparateurs (valeurs >= 50)
    # et extraire les groupes entre eux
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
    
    print(f"Nombre de groupes: {len(groups)}")
    print(f"Premiers groupes: {groups[:10]}")
    
    # Pour chaque groupe, convertir en Morse
    # Hypothèse: 2-3 = point (.), 4-6 = trait (-)
    # Mais les valeurs varient... peut-être que c'est différent
    
    # Regardons les valeurs dans les groupes
    all_group_vals = []
    for g in groups:
        all_group_vals.extend(g)
    
    print(f"\nValeurs dans les groupes (hors séparateurs):")
    print(f"Min: {min(all_group_vals)}, Max: {max(all_group_vals)}")
    print(f"Unique: {sorted(set(all_group_vals))}")
    
    # Compter les occurrences
    counts = Counter(all_group_vals)
    print(f"\nDistribution:")
    for k in sorted(counts.keys()):
        print(f"  {k}: {counts[k]}")