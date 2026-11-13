import struct

# Lire le fichier WAV
with open('audio.wav', 'rb') as f:
    data = f.read()

# Trouver le chunk 'data'
data_start = data.find(b'data')
if data_start != -1:
    data_start += 8
    audio_data = data[data_start:]
    
    # Extraire tous les échantillons
    samples_left = []
    samples_right = []
    for i in range(0, len(audio_data), 4):
        if i + 4 <= len(audio_data):
            left = struct.unpack('<h', audio_data[i:i+2])[0]
            right = struct.unpack('<h', audio_data[i+2:i+4])[0]
            samples_left.append(left)
            samples_right.append(right)
    
    # Regardons les valeurs uniques et leur fréquence
    from collections import Counter
    
    # Combiner les deux canaux
    all_samples = samples_left + samples_right
    
    # Compter les occurrences
    counter = Counter(all_samples)
    
    # Les valeurs les plus fréquentes
    print("Valeurs les plus fréquentes:")
    for val, count in counter.most_common(20):
        print(f"  {val}: {count} fois")
    
    # Regardons les valeurs qui pourraient être des caractères ASCII
    ascii_values = [s for s in all_samples if 32 <= s <= 126]
    print(f"\nNombre de valeurs dans la plage ASCII imprimable: {len(ascii_values)}")
    
    # Regardons les valeurs positives qui pourraient être des caractères
    positive_samples = [s for s in all_samples if s > 0]
    print(f"Nombre d'échantillons positifs: {len(positive_samples)}")
    
    # Regardons les valeurs positives qui sont dans la plage ASCII
    ascii_positive = [s for s in positive_samples if 32 <= s <= 126]
    print(f"Valeurs positives dans la plage ASCII: {len(ascii_positive)}")
    
    # Affichons les premières valeurs positives
    print("\nPremières 50 valeurs positives:")
    pos_list = [s for s in all_samples if s > 0]
    print(pos_list[:50])