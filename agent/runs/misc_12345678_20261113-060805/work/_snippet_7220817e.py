import wave
import struct

with wave.open('audio.wav', 'rb') as wav:
    frames = wav.readframes(wav.getnframes())
    samples = struct.unpack('<' + 'h' * (len(frames) // 2), frames)

# Le titre "12345678" pourrait être:
# 1. Un offset
# 2. Une séquence d'indices pour extraire des échantillons
# 3. Une clé pour décoder

# Essayons d'extraire des échantillons à des positions basées sur "12345678"
# Par exemple, prendre chaque 12e, 3e, 4e, 5e, 6e, 7e, 8e échantillon...
# Ou peut-être que 12345678 est le point de départ

# D'abord, regardons les échantillons non nuls
non_zero = [(i, s) for i, s in enumerate(samples) if s != 0]
print(f"Nombre d'échantillons non nuls: {len(non_zero)}")
print(f"Premiers 20 échantillons non nuls: {non_zero[:20]}")

# Peut-être que le message est encodé dans les valeurs non nulles
# Essayons de convertir les valeurs non nulles en ASCII avec différents offsets
non_zero_values = [s for i, s in non_zero]

for offset in range(0, 256):
    text = ''.join(chr((s + offset) % 256) for s in non_zero_values)
    if "csaw{" in text or "{" in text:
        idx = text.find("{")
        print(f"Trouvé avec offset {offset}: {repr(text[idx-10:idx+50])}")

# Autre idée: peut-être que les valeurs d'échantillon sont des codes ASCII directement
# mais seulement certaines valeurs contiennent le message
# Regardons les valeurs qui sont dans la plage ASCII imprimable (32-126)
print("\n--- Valeurs dans la plage ASCII imprimable ---")
ascii_values = [(i, s) for i, s in enumerate(samples) if 32 <= s <= 126]
print(f"Nombre de valeurs ASCII imprimables: {len(ascii_values)}")
if ascii_values:
    print(f"Premiers 20: {ascii_values[:20]}")
    # Convertir ces valeurs en texte
    text = ''.join(chr(s) for i, s in ascii_values)
    print(f"Texte: {repr(text[:200])}")