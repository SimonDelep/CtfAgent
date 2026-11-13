import wave

# Ouvrir le fichier WAV
with wave.open('audio.wav', 'rb') as wav:
    frames = wav.readframes(wav.getnframes())
    
    # Chercher des motifs de texte ASCII dans les données brutes
    # Convertir les bytes en chaîne ASCII imprimable
    printable = []
    for byte in frames:
        if 32 <= byte <= 126:
            printable.append(chr(byte))
        else:
            printable.append('.')
    
    text = ''.join(printable)
    print("Texte imprimable (premier 500 chars):")
    print(text[:500])
    print()
    
    # Chercher "csaw" ou "flag"
    if 'csaw' in text.lower():
        print("Trouvé 'csaw' dans les données!")
    if 'flag' in text.lower():
        print("Trouvé 'flag' dans les données!")