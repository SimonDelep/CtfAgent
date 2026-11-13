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
    
    # Regardons les valeurs entre 1 et 8 uniquement
    small_seqs = [s for s in seqs if 1 <= s <= 8]
    print(f"Nombre de séquences entre 1 et 8: {len(small_seqs)}")
    print(f"Total de séquences: {len(seqs)}")
    
    # Compter les occurrences de 1-8
    counts = Counter(small_seqs)
    print(f"\nDistribution de 1-8:")
    for i in range(1, 9):
        print(f"  {i}: {counts.get(i, 0)}")
    
    # Peut-être que c'est un encodage où 1-8 représentent des bits ou des symboles
    # Regardons la séquence des valeurs 1-8
    print(f"\nPremières 100 valeurs entre 1-8: {small_seqs[:100]}")
    
    # Essayer de voir si c'est un encodage binaire
    # Par exemple, 1=0, 2=1, ou quelque chose comme ça
    # Ou peut-être que les valeurs paires/impaires ont une signification