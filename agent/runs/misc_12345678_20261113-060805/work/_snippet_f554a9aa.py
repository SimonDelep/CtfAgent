import wave
import struct

with wave.open('audio.wav', 'rb') as wav:
    frames = wav.readframes(wav.getnframes())
    samples = struct.unpack('<' + 'h' * (len(frames) // 2), frames)

# Le titre "12345678" pourrait être:
# 1. Un offset (12345678 % 256 = 114)
# 2. Une séquence d'indices
# 3. Un point de départ

# Essayons avec offset = 12345678 % 256 = 114
offset = 12345678 % 256
print(f"Offset basé sur le titre: {offset}")

text = ''.join(chr((s + offset) % 256) for s in samples)
if "csaw{" in text:
    idx = text.find("csaw{")
    print(f"Trouvé à l'index {idx}: {text[idx:idx+100]}")
else:
    print(f"'csaw{' not found, cherchons '{'")
    if "{" in text:
        idx = text.find("{")
        print(f"Trouvé '{{' à l'index {idx}: {repr(text[idx-20:idx+50])}")

# Essayons aussi avec les valeurs non nulles
non_zero_values = [s for s in samples if s != 0]
text_nz = ''.join(chr((s + offset) % 256) for s in non_zero_values)
if "csaw{" in text_nz:
    idx = text_nz.find("csaw{")
    print(f"Trouvé avec valeurs non nulles à l'index {idx}: {text_nz[idx:idx+100]}")
else:
    if "{" in text_nz:
        idx = text_nz.find("{")
        print(f"Trouvé '{{' avec non nulles à l'index {idx}: {repr(text_nz[idx-20:idx+50])}")

# Autre idée: peut-être que 12345678 est le point de départ dans le fichier
# Prenons les échantillons à partir de l'index 12345678
start = 12345678
if start < len(samples):
    chunk = samples[start:start+200]
    print(f"\nÉchantillons à partir de l'index {start}: {chunk[:50]}")
    # Essayons de convertir avec différents offsets
    for off in range(0, 256):
        text = ''.join(chr((s + off) % 256) for s in chunk)
        if "csaw{" in text or "{" in text:
            print(f"Avec offset {off}: {repr(text[:100])}")