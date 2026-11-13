import wave
import struct

# Lire le fichier WAV
with wave.open('audio.wav', 'rb') as wav:
    data = wav.readframes(wav.getnframes())
    samples = struct.unpack('<' + 'h' * (len(data) // 2), data)

# Séparer les canaux
left = samples[0::2]
right = samples[1::2]

# Chercher des séquences de caractères imprimables dans les valeurs brutes
def find_printable_sequences(samples, min_len=10):
    sequences = []
    current_seq = []
    for i, s in enumerate(samples):
        if 32 <= s <= 126:
            current_seq.append((i, s, chr(s)))
        else:
            if len(current_seq) >= min_len:
                sequences.append(current_seq)
            current_seq = []
    if len(current_seq) >= min_len:
        sequences.append(current_seq)
    return sequences

left_seqs = find_printable_sequences(left)
right_seqs = find_printable_sequences(right)

print("Left printable sequences:")
for seq in left_seqs[:10]:
    chars = ''.join(c for _, _, c in seq)
    print(f"  Pos {seq[0][0]}: {chars[:50]}... (len={len(seq)})")

print("\nRight printable sequences:")
for seq in right_seqs[:10]:
    chars = ''.join(c for _, _, c in seq)
    print(f"  Pos {seq[0][0]}: {chars[:50]}... (len={len(seq)})")
