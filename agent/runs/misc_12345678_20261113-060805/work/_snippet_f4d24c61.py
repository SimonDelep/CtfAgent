import wave
import struct

with wave.open('audio.wav', 'rb') as wav:
    frames = wav.readframes(wav.getnframes())
    samples = struct.unpack('<' + 'h' * (len(frames) // 2), frames)

# Séparer les échantillons par canal (stéréo)
left = samples[::2]
right = samples[1::2]

print(f"Canal gauche: {len(left)} échantillons, min={min(left)}, max={max(left)}")
print(f"Canal droit: {len(right)} échantillons, min={min(right)}, max={max(right)}")

# Peut-être que le message est dans un seul canal
# Essayons de convertir chaque canal en ASCII avec différents offsets
for channel_name, channel in [("gauche", left), ("droit", right)]:
    for offset in range(0, 256):
        text = ''.join(chr((s + offset) % 256) for s in channel)
        if "csaw{" in text:
            idx = text.find("csaw{")
            print(f"Trouvé dans canal {channel_name} avec offset {offset}: {text[idx:idx+100]}")
            break
    else:
        # Cherchons juste "{"
        for offset in range(0, 256):
            text = ''.join(chr((s + offset) % 256) for s in channel)
            if "{" in text:
                idx = text.find("{")
                print(f"Trouvé '{{' dans canal {channel_name} avec offset {offset}: {repr(text[idx-20:idx+50])}")
                break

# Autre idée: peut-être que les valeurs sont des codes ASCII décalés
# Cherchons des séquences de valeurs qui pourraient former "csaw{"
# c=99, s=115, a=97, w=119, {=123
target = [99, 115, 97, 119, 123]
print(f"\nRecherche de séquence {target} dans les échantillons...")
for i in range(len(samples) - 4):
    if samples[i:i+5] == tuple(target):
        print(f"Trouvé à l'index {i}")
        break
else:
    print("Séquence exacte non trouvée")

# Peut-être que c'est dans les valeurs absolues
abs_samples = [abs(s) for s in samples]
for i in range(len(abs_samples) - 4):
    if abs_samples[i:i+5] == tuple(target):
        print(f"Trouvé avec valeurs absolues à l'index {i}")
        break