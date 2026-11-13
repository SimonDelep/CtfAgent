import wave
import struct

# Re-lisons le fichier WAV
with wave.open('audio.wav', 'rb') as w:
    print(f"Channels: {w.getnchannels()}")
    print(f"Sample width: {w.getsampwidth()}")
    print(f"Frame rate: {w.getframerate()}")
    print(f"Num frames: {w.getnframes()}")
    
    # Lire tous les frames
    frames = w.readframes(w.getnframes())
    print(f"Total bytes: {len(frames)}")
    
    # Convertir en samples
    if w.getsampwidth() == 2:
        samples = struct.unpack('<' + 'h' * (len(frames)//2), frames)
        print(f"Total samples: {len(samples)}")
        
        # Vérifier les valeurs min/max
        print(f"Min sample: {min(samples)}")
        print(f"Max sample: {max(samples)}")
        
        # Afficher les 100 premiers samples
        print(f"First 100 samples: {samples[:100]}")
        
        # Chercher le motif "12345678" dans les samples
        # Peut-être que les samples contiennent cette séquence
        target = [1, 2, 3, 4, 5, 6, 7, 8]
        for i in range(len(samples) - 8):
            if list(samples[i:i+8]) == target:
                print(f"Found 12345678 at position {i}")
                break
        else:
            print("12345678 not found as consecutive samples")