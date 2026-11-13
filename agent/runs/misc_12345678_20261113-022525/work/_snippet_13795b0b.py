import wave
import struct
from collections import Counter

# Lire le fichier WAV
with wave.open('audio.wav', 'rb') as wav:
    raw_data = wav.readframes(wav.getnframes())
    samples = struct.unpack(f'{wav.getnframes() * wav.getnchannels()}h', raw_data)

# Filtrer seulement les valeurs dont la valeur absolue est entre 1 et 8
filtered = [s for s in samples if 1 <= abs(s) <= 8]

# Approche 1: Mapping valeur absolue -> lettre (1=A, 2=B, etc.)
mapping1 = {i: chr(ord('A') + i - 1) for i in range(1, 9)}
text1 = ''.join(mapping1[abs(s)] for s in filtered[:200])
print("Approche 1 (|valeur| -> A-H):")
print(text1)

# Approche 2: Signe + valeur absolue comme symbole unique
# +1, -1, +2, -2, ... +8, -8 = 16 symboles
# Essayons de mapper à des lettres
symbols = []
for s in filtered:
    if s > 0:
        symbols.append(f"+{s}")
    else:
        symbols.append(f"{s}")

# Compter la fréquence de chaque symbole
sym_counts = Counter(symbols)
print("\nFréquences des symboles (signe+valeur):")
for sym, cnt in sym_counts.most_common(16):
    print(f"  {sym}: {cnt}")

# Approche 3: Convertir en binaire - signe comme bit, valeur comme autre chose
# Ou peut-être que la valeur absolue indique le nombre de bits, et le signe indique 0/1

# Approche 4: Utiliser seulement le signe comme bit (positif=1, négatif=0)
bits = [1 if s > 0 else 0 for s in filtered[:100]]
print(f"\nApproche 4 (signe comme bit): {bits[:50]}")

# Convertir en bytes
bit_str = ''.join(str(b) for b in bits)
print(f"String binaire: {bit_str[:80]}")
