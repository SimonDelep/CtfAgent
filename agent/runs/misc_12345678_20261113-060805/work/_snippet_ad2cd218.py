import wave
import struct

with wave.open('audio.wav', 'rb') as wav:
    frames = wav.readframes(wav.getnframes())
    samples = struct.unpack('<' + 'h' * (len(frames) // 2), frames)

# Avec offset 246, on a vu quelque chose d'intéressant
# Cherchons "csaw{" avec offset 246
offset = 246
text = ''.join(chr((s + offset) % 256) for s in samples)

# Cherchons "csaw{" ou des patterns similaires
print("Recherche de 'csaw{' avec offset 246:")
if "csaw{" in text:
    idx = text.find("csaw{")
    print(f"Trouvé à l'index {idx}")
    print(f"Flag: {text[idx:idx+100]}")
else:
    # Cherchons des patterns partiels
    for pattern in ["csaw", "csa", "saw", "c{", "cs{"]:
        if pattern in text:
            idx = text.find(pattern)
            print(f"Trouvé '{pattern}' à l'index {idx}: {repr(text[idx:idx+50])}")

# Peut-être que le message est dans les valeurs non nulles seulement
non_zero_values = [s for s in samples if s != 0]
text_nz = ''.join(chr((s + offset) % 256) for s in non_zero_values)
print("\nAvec valeurs non nulles seulement:")
if "csaw{" in text_nz:
    idx = text_nz.find("csaw{")
    print(f"Trouvé à l'index {idx}")
    print(f"Flag: {text_nz[idx:idx+100]}")
else:
    for pattern in ["csaw", "csa", "saw", "c{", "cs{", "{"]:
        if pattern in text_nz:
            idx = text_nz.find(pattern)
            print(f"Trouvé '{pattern}' à l'index {idx}: {repr(text_nz[idx:idx+50])}")

# Essayons aussi de chercher "}" pour trouver la fin du flag
if "}" in text_nz:
    idx = text_nz.find("}")
    print(f"\nTrouvé '}}' à l'index {idx}: {repr(text_nz[max(0,idx-50):idx+10])}")