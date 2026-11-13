import wave
import struct
from collections import Counter

# Lire le fichier WAV
with wave.open('audio.wav', 'rb') as wav:
    raw_data = wav.readframes(wav.getnframes())
    samples = struct.unpack(f'{wav.getnframes() * wav.getnchannels()}h', raw_data)

# Filtrer seulement les valeurs dont la valeur absolue est entre 1 et 8
filtered = [s for s in samples if 1 <= abs(s) <= 8]

# Essai: utiliser seulement la valeur absolue, ignorer le signe
abs_values = [abs(s) for s in filtered]

# Peut-être que c'est un encodage où chaque valeur représente un caractère
# 1-8 = 8 symboles, donc 3 bits par symbole
# Ou peut-être que c'est un encodage de type "base 8"

# Regardons si les séquences de valeurs forment des motifs
# Par exemple, cherchons des séquences répétitives

# Autre idée: peut-être que le signe indique si on doit incrémenter ou décrémenter un compteur
# et la valeur absolue indique de combien

# Ou peut-être que c'est un encodage où chaque paire de valeurs (valeur absolue) forme un caractère
# 8 * 8 = 64 combinaisons, ce qui pourrait encoder des caractères ASCII

# Regardons les paires de valeurs absolues
pairs = [(abs_values[i], abs_values[i+1]) for i in range(0, len(abs_values)-1, 2)]

# Compter les paires les plus fréquentes
pair_counts = Counter(pairs)
print("Paires les plus fréquentes:")
for pair, cnt in pair_counts.most_common(20):
    print(f"  {pair}: {cnt}")

# Essayer de mapper les paires à des caractères
# Si on considère que (a, b) -> (a-1)*8 + (b-1) = index 0-63
def pair_to_char(p):
    idx = (p[0] - 1) * 8 + (p[1] - 1)
    # Essayons de mapper à des caractères ASCII
    # Peut-être que idx + 32 donne des caractères imprimables
    return chr(idx + 32) if 0 <= idx < 64 else '?'

chars_from_pairs = ''.join(pair_to_char(p) for p in pairs[:100])
print(f"\nCaractères à partir des paires: {chars_from_pairs}")
