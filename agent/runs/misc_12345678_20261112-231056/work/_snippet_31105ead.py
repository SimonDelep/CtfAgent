import struct
import math

# Lire le fichier WAV
with open('audio.wav', 'rb') as f:
    data = f.read()

# Trouver le chunk 'data'
data_start = data.find(b'data')
if data_start != -1:
    data_start += 8
    audio_data = data[data_start:]
    
    # Extraire tous les échantillons (stéréo, interleaved)
    samples = []
    for i in range(0, len(audio_data), 2):
        if i + 2 <= len(audio_data):
            val = struct.unpack('<h', audio_data[i:i+2])[0]
            samples.append(val)
    
    # Calculer l'amplitude absolue moyenne pour détecter les silences
    # ou regarder la distribution des valeurs
    
    # Regarder la distribution des valeurs
    min_val = min(samples)
    max_val = max(samples)
    print("Min:", min_val, "Max:", max_val)
    
    # Compter les valeurs proches de 0 (silence)
    zero_count = sum(1 for s in samples if abs(s) < 10)
    print("Échantillons proches de 0:", zero_count, "sur", len(samples))
    
    # Peut-être que le message est dans les changements de valeur
    # Regarder les différences entre échantillons consécutifs
    diffs = [samples[i+1] - samples[i] for i in range(min(1000, len(samples)-1))]
    print("Premières différences:", diffs[:50])