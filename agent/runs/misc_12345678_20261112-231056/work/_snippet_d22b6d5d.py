import wave

with wave.open('audio.wav', 'rb') as wav:
    data = wav.readframes(wav.getnframes())

# Bytes pairs
even_bytes = [data[i] for i in range(0, len(data), 2)]

print("Premiers 100 bytes pairs:", even_bytes[:100])

# Distribution
from collections import Counter
counter = Counter(even_bytes[:1000])
print("\nDistribution des valeurs (premiers 1000 bytes pairs):")
for val, count in sorted(counter.items())[:20]:
    print(f"  {val}: {count}")

# Peut-être que les bytes pairs contiennent directement le message
# Regardons si on peut trouver 'csaw{' ou '{'
for i, b in enumerate(even_bytes[:200]):
    if b == 123:  # '{'
        print(f"Trouvé '{' à l'index {i}")
    if b == 99:  # 'c'
        print(f"Trouvé 'c' à l'index {i}")