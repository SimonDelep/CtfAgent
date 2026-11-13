import wave
import struct

# Ouvrir le fichier WAV
with wave.open('audio.wav', 'rb') as wav:
    params = wav.getparams()
    print(f"Nombre de canaux: {params.nchannels}")
    print(f"Fréquence d'échantillonnage: {params.framerate}")
    print(f"Échantillons par seconde: {params.framerate}")
    print(f"Nombre d'échantillons: {params.nframes}")
    print(f"Largeur d'échantillon: {params.sampwidth} octets")
    
    # Lire les données
    frames = wav.readframes(params.nframes)
    
    # Si stéréo, chaque échantillon est 2 octets par canal (16-bit)
    if params.nchannels == 2 and params.sampwidth == 2:
        # Décompresser les données
        samples = struct.unpack('<' + 'h' * (len(frames) // 2), frames)
        # Séparer les canaux
        left = samples[0::2]
        right = samples[1::2]
        print(f"Nombre d'échantillons par canal: {len(left)}")
        
        # Analyser le canal droit pour les silences
        # Un silence est une séquence de valeurs proches de 0
        # Trouver les séquences de silences
        
        def find_silence_sequences(samples, threshold=100):
            sequences = []
            current_len = 0
            in_silence = False
            
            for s in samples:
                if abs(s) < threshold:
                    if not in_silence:
                        in_silence = True
                        current_len = 1
                    else:
                        current_len += 1
                else:
                    if in_silence:
                        sequences.append(current_len)
                        in_silence = False
                        current_len = 0
            if in_silence:
                sequences.append(current_len)
            return sequences
        
        # Tester avec différents seuils
        for thresh in [50, 100, 200]:
            seqs = find_silence_sequences(right, thresh)
            print(f"\nSeuil {thresh}: {len(seqs)} séquences de silence")
            if seqs:
                print(f"Longueurs minimales/maximales: {min(seqs)}/{max(seqs)}")
                # Afficher les 50 premières longueurs
                print(f"Premières longueurs: {seqs[:50]}")
                # Compter les occurrences de chaque longueur
                from collections import Counter
                counts = Counter(seqs)
                print(f"Distribution: {dict(sorted(counts.items()))}")