import wave
import struct

# Ouvrir le fichier WAV
with wave.open('audio.wav', 'rb') as wf:
    print(f"Nombre de canaux: {wf.getnchannels()}")
    print(f"Taille d'échantillon: {wf.getsampwidth()} bytes")
    print(f"Fréquence d'échantillonnage: {wf.getframerate()} Hz")
    print(f"Nombre de frames: {wf.getnframes()}")
    print(f"Durée: {wf.getnframes() / wf.getframerate():.2f} secondes")
    
    # Lire les données brutes
    data = wf.readframes(wf.getnframes())
    print(f"Taille des données: {len(data)} bytes")
    
    # Convertir en échantillons
    if wf.getsampwidth() == 2:
        samples = struct.unpack('<' + 'h' * (len(data) // 2), data)
        print(f"Nombre d'échantillons: {len(samples)}")
        
        # Trouver les séquences de zéros (silence)
        zero_sequences = []
        current_len = 0
        for i, s in enumerate(samples):
            if s == 0:
                current_len += 1
            else:
                if current_len > 5:  # Seulement les séquences significatives
                    zero_sequences.append((i - current_len, current_len))
                current_len = 0
        if current_len > 5:
            zero_sequences.append((len(samples) - current_len, current_len))
        
        print(f"\nSéquences de zéros (> 5 échantillons):")
        for start, length in zero_sequences[:20]:
            print(f"  Position {start}: {length} échantillons")
        
        print(f"\nTotal de séquences de zéros: {len(zero_sequences)}")
        
        # Afficher les longueurs uniques
        lengths = sorted(set(l for _, l in zero_sequences))
        print(f"Longueurs uniques: {lengths}")