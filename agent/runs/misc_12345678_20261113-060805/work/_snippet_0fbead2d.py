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
    
    # Combiner les deux canaux
    all_samples = samples_left + samples_right
    
    # Regardons les valeurs qui sont exactement dans la plage ASCII imprimable
    # et voyons si elles forment un message
    ascii_chars = []
    for s in all_samples:
        if 32 <= s <= 126:
            ascii_chars.append(chr(s))
    
    # Affichons le message complet
    message = ''.join(ascii_chars)
    print(f"Longueur du message: {len(message)}")
    
    # Cherchons des motifs comme "csaw" ou "{"
    if "csaw" in message.lower():
        print("Trouvé 'csaw' dans le message!")
        idx = message.lower().find("csaw")
        print(f"Position: {idx}")
        print(f"Contexte: {message[max(0, idx-10):idx+50]}")
    
    if "{" in message:
        idx = message.find("{")
        print(f"Trouvé '{{' à la position {idx}")
        print(f"Contexte: {message[max(0, idx-10):idx+50]}")
    
    # Affichons le début du message
    print("\nDébut du message:")
    print(message[:500])