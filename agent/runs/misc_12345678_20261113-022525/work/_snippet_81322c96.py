import wave
import struct
from collections import Counter

# Lire le fichier WAV
with wave.open('audio.wav', 'rb') as wav:
    raw_data = wav.readframes(wav.getnframes())
    samples = struct.unpack(f'{wav.getnframes() * wav.getnchannels()}h', raw_data)

# Filtrer seulement les valeurs dont la valeur absolue est entre 1 et 8
filtered = [s for s in samples if 1 <= abs(s) <= 8]

# Afficher les 100 premières valeurs
print("Premières 100 valeurs filtrées:")
print(filtered[:100])

# Vérifier la longueur
print(f"\nLongueur de la séquence filtrée: {len(filtered)}")

# Essayer de mapper les valeurs à des lettres
# Hypothèse: valeur absolue 1-8 = A-H, signe détermine quelque chose
# Ou peut-être que +1, -1, +2, -2, ... +8, -8 = 16 symboles différents

# Regardons la distribution des transitions
transitions = []
for i in range(len(filtered)-1):
    transitions.append((filtered[i], filtered[i+1]))

# Compter les transitions de signe
pos_to_neg = sum(1 for a, b in transitions if a > 0 and b < 0)
neg_to_pos = sum(1 for a, b in transitions if a < 0 and b > 0)
pos_to_pos = sum(1 for a, b in transitions if a > 0 and b > 0)
neg_to_neg = sum(1 for a, b in transitions if a < 0 and b < 0)

print(f"\nTransitions:")
print(f"  pos->neg: {pos_to_neg}")
print(f"  neg->pos: {neg_to_pos}")
print(f"  pos->pos: {pos_to_pos}")
print(f"  neg->neg: {neg_to_neg}")
