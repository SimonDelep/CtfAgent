import wave

# Ouvrir le fichier WAV
with wave.open('audio.wav', 'rb') as wav:
    frames = wav.readframes(wav.getnframes())
    
    # Essayer de lire le fichier comme s'il contenait du texte ASCII directement
    # Peut-être que les données audio sont en fait du texte encodé
    # Regardons les bytes bruts et cherchons des motifs
    
    # Chercher "csaw{" dans les données brutes
    data = frames
    for i in range(len(data) - 5):
        if data[i:i+5] == b'csaw{':
            print(f"Trouvé 'csaw{{' à la position {i}")
            print("Contexte:", data[i:i+50])
            break
    
    # Chercher "flag"
    for i in range(len(data) - 4):
        if data[i:i+4] == b'flag':
            print(f"Trouvé 'flag' à la position {i}")
            print("Contexte:", data[i:i+50])
            break