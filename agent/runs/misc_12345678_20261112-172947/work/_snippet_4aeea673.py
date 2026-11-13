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
    
    # Pour chaque groupe, extraire les valeurs uniques et voir si c'est un motif
    # Peut-être que chaque groupe représente un caractère
    
    # Regardons les groupes identiques
    from collections import defaultdict
    group_counts = defaultdict(int)
    for g in groups:
        group_counts[tuple(g)] += 1
    
    # Trouver les groupes les plus fréquents
    sorted_groups = sorted(group_counts.items(), key=lambda x: -x[1])
    print("Groupes les plus fréquents:")
    for g, count in sorted_groups[:10]:
        print(f"  {count}x: {g[:20]}...")
    
    # Peut-être que les groupes identiques représentent le même caractère
    # Regardons les groupes qui apparaissent plusieurs fois
    print(f"\nNombre de groupes uniques: {len(group_counts)}")
    print(f"Nombre total de groupes: {len(groups)}")