import struct
import wave
from collections import Counter

with wave.open('audio.wav', 'rb') as wav:
    raw_data = wav.readframes(wav.getnframes())

samples = struct.unpack('<' + 'h' * (len(raw_data) // 2), raw_data)

# Extraire les valeurs positives entre 1 et 8
positive_sequence = [s for s in samples if 1 <= s <= 8]

# Peut-être que c'est un code où chaque valeur représente un caractère
# et qu'il faut trouver le mapping correct

# Regardons la séquence complète et essayons de trouver des patterns
# Peut-être que le message est juste la séquence de valeurs elle-même

# Essayons de voir si la séquence contient "csaw" en cherchant des patterns
# Peut-être que c'est un code où on doit lire les valeurs différemment

# Autre idée: peut-être que c'est un code où chaque valeur représente un caractère
# et qu'il faut appliquer une substitution monoalphabétique

# Regardons la distribution des valeurs
counts = Counter(positive_sequence)
print("Distribution des valeurs:")
for v in sorted(counts.keys()):
    print(f"  {v}: {counts[v]} ({counts[v]/len(positive_sequence)*100:.2f}%)")

# La distribution est décroissante: 1 > 2 > 3 > 4 > 5 > 6 > 7 > 8
# En anglais, la distribution typique est: E > T > A > O > I > N > S > H > R > D > L > C > U > M > W > F > G > Y > P > B > V > K > J > X > Q > Z

# Peut-être que 1 = E, 2 = T, 3 = A, etc.
# Essayons de mapper les valeurs aux lettres les plus fréquentes en anglais

# Mapping hypothétique: 1->E, 2->T, 3->A, 4->O, 5->I, 6->N, 7->S, 8->H
mapping = {1: 'E', 2: 'T', 3: 'A', 4: 'O', 5: 'I', 6: 'N', 7: 'S', 8: 'H'}
decoded = ''.join(mapping.get(v, '?') for v in positive_sequence[:200])
print(f"\nMapping 1=E, 2=T, 3=A, 4=O, 5=I, 6=N, 7=S, 8=H: {decoded}")

# Essayons d'autres mappings basés sur la fréquence
# Peut-être que 1 = E, 2 = T, 3 = A, 4 = O, 5 = I, 6 = N, 7 = S, 8 = R
mapping2 = {1: 'E', 2: 'T', 3: 'A', 4: 'O', 5: 'I', 6: 'N', 7: 'S', 8: 'R'}
decoded2 = ''.join(mapping2.get(v, '?') for v in positive_sequence[:200])
print(f"Mapping 1=E, 2=T, 3=A, 4=O, 5=I, 6=N, 7=S, 8=R: {decoded2}")

# Peut-être que c'est un code où les valeurs 1-8 représentent des lettres A-H
# et qu'il faut appliquer une substitution monoalphabétique pour obtenir le message

# Regardons si on peut trouver "csaw" en cherchant des patterns dans la séquence
# Peut-être que c'est un code où on doit lire les valeurs différemment

# Autre idée: peut-être que c'est un code où chaque valeur représente un caractère
# et qu'il faut trouver le mapping correct en cherchant "csaw" ou "flag"

# Essayons de trouver un mapping qui donne "csaw" ou "flag"
# en cherchant des patterns dans la séquence

# Regardons les 4 premières valeurs de la séquence
print(f"\nPremières 10 valeurs: {positive_sequence[:10]}")

# Si le message commence par "csaw", alors les 4 premières valeurs devraient mapper à c, s, a, w
# Essayons de trouver un mapping qui donne "csaw" pour les 4 premières valeurs

# Les 4 premières valeurs sont: 2, 1, 2, 3
# Si 2->c, 1->s, 2->a, 3->w, alors 2 devrait mapper à c et a, ce qui est impossible
# Donc le message ne commence pas par "csaw"

# Peut-être que le message commence par "flag"
# Les 4 premières valeurs sont: 2, 1, 2, 3
# Si 2->f, 1->l, 2->a, 3->g, alors 2 devrait mapper à f et a, ce qui est impossible
# Donc le message ne commence pas par "flag" non plus

# Peut-être que le message est plus long et que "csaw" ou "flag" apparaît plus tard

# Regardons la séquence complète et essayons de trouver des patterns
# Peut-être que c'est un code où chaque valeur représente un caractère
# et qu'il faut appliquer une substitution monoalphabétique

# Essayons de voir si la séquence contient "csaw" en cherchant des patterns
# en utilisant tous les mappings possibles

# D'abord, trouvons toutes les séquences de 4 valeurs consécutives
from collections import Counter
four_seqs = Counter()
for i in range(len(positive_sequence) - 3):
    seq = tuple(positive_sequence[i:i+4])
    four_seqs[seq] += 1

print(f"\nSéquences de 4 valeurs les plus fréquentes:")
for seq, count in four_seqs.most_common(10):
    print(f"  {seq}: {count}")

# Peut-être que la séquence la plus fréquente correspond à "the" ou un autre mot courant