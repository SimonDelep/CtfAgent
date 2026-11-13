import wave
import struct
from collections import Counter

# Ouvrir le fichier WAV
with wave.open('audio.wav', 'rb') as wav:
    frames = wav.readframes(wav.getnframes())
    samples = struct.unpack('<' + 'h' * (len(frames) // 2), frames)
    right = samples[1::2]  # Canal droit
    
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
    
    # Ignorer la première séquence (très longue, début du fichier)
    seqs = seqs[1:]
    
    # Filtrer les séquences de longueur 1 (bruit/separateurs)
    # et garder seulement les séquences >= 2
    filtered = [s for s in seqs if s >= 2]
    
    print(f"Nombre de séquences filtrées (>=2): {len(filtered)}")
    print(f"Premières 100 longueurs: {filtered[:100]}")
    
    # Compter les occurrences
    counts = Counter(filtered)
    print(f"\nDistribution des longueurs (>=2):")
    for k in sorted(counts.keys())[:30]:
        print(f"  {k}: {counts[k]}")
    
    # Essayer de mapper les longueurs à Morse
    # Hypothèse: 2-3 = point, 4-6 = trait, 7+ = séparateur de mot
    # Ou peut-être que les longueurs elles-mêmes encodent directement
    
    # Regardons les valeurs uniques
    unique_vals = sorted(set(filtered))
    print(f"\nValeurs uniques: {unique_vals[:50]}")