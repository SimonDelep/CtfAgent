import wave
import struct

# Ouvrir le fichier WAV
with wave.open('audio.wav', 'rb') as wav:
    params = wav.getparams()
    print(f"Canal: {params.nchannels}, Échantillons: {params.nframes}, Profondeur: {params.sampwidth} bytes, Fréquence: {params.framerate}")
    
    # Lire les données brutes
    data = wav.readframes(params.nframes)
    print(f"Taille des données: {len(data)} bytes")
    
    # Extraire les bits LSB de chaque byte
    lsb_bits = [byte & 1 for byte in data]
    
    # Regarder autour de l'index 1121
    start = max(0, 1121 - 20)
    end = min(len(lsb_bits), 1121 + 100)
    
    print(f"\nBits LSB autour de l'index 1121:")
    print(f"Index 1121: {lsb_bits[1121]}")
    
    # Convertir en bytes (8 bits = 1 byte)
    bits_str = ''.join(map(str, lsb_bits[start:end]))
    print(f"Bits (20 avant à 100 après 1121): {bits_str[:100]}...")
    
    # Convertir en texte ASCII
    text = ''
    for i in range(start, end - 7, 8):
        byte_val = int(''.join(map(str, lsb_bits[i:i+8])), 2)
        text += chr(byte_val) if 32 <= byte_val < 127 else '.'
    
    print(f"\nTexte brut LSB autour de 1121:")
    print(text[:100])
