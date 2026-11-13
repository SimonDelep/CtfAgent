import wave
import struct

with wave.open('audio.wav', 'rb') as w:
    frames = w.readframes(w.getnframes())
    samples = struct.unpack('<' + 'h' * (len(frames)//2), frames)

# Essayer de prendre chaque 8ème sample et extraire son LSB
# Ou peut-être que "12345678" signifie qu'il y a 8 canaux de bits

# Autre idée : peut-être que le message est dans les bits de poids fort (bits 15-8)
# Ou peut-être que c'est une modulation de fréquence

# Regardons la distribution des valeurs
from collections import Counter

# Compter combien de samples ont LSB=0 vs LSB=1
lsb_counts = Counter([s & 1 for s in samples])
print(f"LSB distribution: {lsb_counts}")

# Peut-être que le message est encodé par la parité des samples
# Ou peut-être que c'est une séquence de valeurs spécifiques

# Essayons de voir si les samples contiennent des valeurs qui correspondent à des caractères ASCII
# en utilisant seulement les 8 bits de poids faible
low_bytes = [s & 0xFF for s in samples]

# Chercher des séquences de bytes imprimables
def find_printable_sequences(data, min_len=10):
    sequences = []
    current = []
    for b in data:
        if 32 <= b < 127:
            current.append(b)
        else:
            if len(current) >= min_len:
                sequences.append(bytes(current))
            current = []
    if len(current) >= min_len:
        sequences.append(bytes(current))
    return sequences

printable_seqs = find_printable_sequences(low_bytes, 10)
print(f"\nPrintable sequences in low bytes (min 10 chars):")
for seq in printable_seqs[:10]:
    print(seq)

# Même chose pour les LSB
printable_seqs_lsb = find_printable_sequences([s & 1 for s in samples], 10)
print(f"\nPrintable sequences in LSB (min 10 chars):")
for seq in printable_seqs_lsb[:10]:
    print(seq)