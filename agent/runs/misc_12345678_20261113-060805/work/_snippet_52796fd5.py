import struct

# Lire le fichier WAV
with open('audio.wav', 'rb') as f:
    data = f.read()

# Trouver le chunk 'data'
data_start = data.find(b'data')
if data_start != -1:
    data_start += 8  # Après 'data' et la taille
    audio_data = data[data_start:]
    print(f"Longueur des données audio: {len(audio_data)} octets")
    
    # C'est stéréo 16-bit, donc 4 octets par échantillon (2 canaux x 2 octets)
    # Essayons d'extraire les valeurs
    samples = []
    for i in range(0, len(audio_data), 4):
        if i + 4 <= len(audio_data):
            left = struct.unpack('<h', audio_data[i:i+2])[0]
            right = struct.unpack('<h', audio_data[i+2:i+4])[0]
            samples.append((left, right))
    
    print(f"Nombre d'échantillons: {len(samples)}")
    
    # Regardons les premières valeurs
    print("Premiers 50 échantillons (gauche, droite):")
    for i, (l, r) in enumerate(samples[:50]):
        print(f"  {i}: ({l:6d}, {r:6d})")