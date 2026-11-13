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
        groups.append(groups)
    
    # Regardons la structure des groupes - peut-être que chaque groupe est un caractère
    # et les valeurs dans le groupe sont des bits
    
    # Compter le nombre d'éléments dans chaque groupe
    group_lengths = [len(g) for g in groups]
    print(f"Longueurs des groupes: {group_lengths[:20]}")
    print(f"Longueur moyenne: {sum(group_lengths)/len(group_lengths):.2f}")
    
    # Peut-être que les groupes ont une longueur fixe et représentent des caractères
    # Regardons les groupes de longueur similaire
    from collections import defaultdict
    groups_by_len = defaultdict(list)
    for i, g in enumerate(groups):
        groups_by_len[len(g)].append(i)
    
    print(f"\nGroupes par longueur:")
    for l in sorted(groups_by_len.keys())[:10]:
        print(f"  Longueur {l}: {len(groups_by_len[l])} groupes, indices: {groups_by_len[l][:5]}")