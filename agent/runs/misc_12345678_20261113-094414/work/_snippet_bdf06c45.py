from PIL import Image

img = Image.open('spectrogram.png')
w, h = img.size
print(f"Taille originale: {w}x{h}")

# Gardons une hauteur raisonnable, disons 200 pixels, et ajustons la largeur
new_height = 200
new_width = int(w * new_height / h)
print(f"Nouvelle taille: {new_width}x{new_height}")

resized = img.resize((new_width, new_height), Image.LANCZOS)
resized.save('spectrogram_resized2.png')

# Lisons aussi le fichier WAV pour extraire les données brutes et chercher du texte
import struct

with open('audio.wav', 'rb') as f:
    data = f.read()

# Trouver le chunk 'data'
idx = data.find(b'data')
if idx != -1:
    chunk_size = struct.unpack('<I', data[idx+4:idx+8])[0]
    audio_data = data[idx+8:idx+8+chunk_size]
    print(f"Taille des données audio: {len(audio_data)}")
    
    # Les échantillons sont en 16-bit signed
    num_samples = len(audio_data) // 2
    print(f"Nombre d'échantillons: {num_samples}")
    
    # Séparer les canaux (stéréo = 2 canaux)
    # Chaque échantillon = 2 bytes * 2 canaux = 4 bytes par frame
    num_frames = num_samples // 2
    print(f"Nombre de frames: {num_frames}")
    
    # Extraire les canaux
    left_channel = []
    right_channel = []
    
    for i in range(num_frames):
        offset = i * 4
        left = struct.unpack('<h', audio_data[offset:offset+2])[0]
        right = struct.unpack('<h', audio_data[offset+2:offset+4])[0]
        left_channel.append(left)
        right_channel.append(right)
    
    # Convertir en valeurs ASCII (décalage pour centrer autour de 0)
    # Les valeurs audio vont de -32768 à 32767
    # Essayons de voir si certaines valeurs correspondent à des caractères ASCII
    
    # Pour le canal droit, cherchons des plages de valeurs qui pourraient être du texte
    right_values = [v + 32768 for v in right_channel]  # Décalage pour avoir des valeurs positives
    print(f"Valeurs min/max canal droit: {min(right_values)} / {max(right_values)}")
    
    # Essayons de convertir directement les valeurs du canal droit en caractères
    # En supposant que les valeurs sont déjà dans la plage ASCII
    text_candidate = ""
    for v in right_channel:
        if 32 <= v <= 126:
            text_candidate += chr(v)
        else:
            text_candidate += '?'
    
    # Afficher des segments du texte candidat
    print("Texte candidat (canal droit) - premiers 500 chars:")
    print(text_candidate[:500])
    print("...")
    print("Texte candidat - derniers 500 chars:")
    print(text_candidate[-500:])