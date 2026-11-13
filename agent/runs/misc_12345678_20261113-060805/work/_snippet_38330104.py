import wave
import struct

with wave.open('audio.wav', 'rb') as wav:
    frames = wav.readframes(wav.getnframes())
    samples = struct.unpack('<' + 'h' * (len(frames) // 2), frames)

# Le titre est "12345678" - peut-être que c'est un offset ou une clé
# Essayons de trouver des séquences de valeurs qui, avec un certain offset, forment "csaw{"

# D'abord, cherchons où se trouve la valeur qui pourrait correspondre à '{' (ASCII 123)
# Si on suppose que les valeurs d'échantillon + offset = ASCII, alors:
# sample + offset = 123 => sample = 123 - offset

# Essayons différents offsets et voyons si on trouve "csaw{"
target = "csaw{"
target_codes = [ord(c) for c in target]
print(f"Codes ASCII de '{target}': {target_codes}")

# Cherchons des séquences de 5 échantillons consécutifs qui pourraient former "csaw{"
# avec différents offsets
for offset in range(-100, 100):
    expected_samples = [c - offset for c in target_codes]
    # Chercher cette séquence dans samples
    for i in range(len(samples) - 4):
        if samples[i:i+5] == tuple(expected_samples):
            print(f"Trouvé avec offset {offset} à l'index {i}: {samples[i:i+5]}")
            # Affichons un peu de contexte
            context = samples[max(0, i-10):i+15]
            print(f"Contexte: {context}")
            # Convertissons avec cet offset
            text = ''.join(chr(s + offset) for s in samples[i:i+50])
            print(f"Texte décodé: {repr(text)}")
            break
    else:
        continue
    break

# Si on ne trouve pas, essayons une autre approche: convertir toutes les valeurs en ASCII
# et chercher "csaw{" dans le résultat
print("\n--- Recherche directe ---")
for offset in range(0, 256):
    text = ''.join(chr((s + offset) % 256) for s in samples)
    if "csaw{" in text:
        idx = text.find("csaw{")
        print(f"Trouvé avec offset {offset} à l'index {idx}")
        print(f"Flag potentiel: {text[idx:idx+50]}")
        break