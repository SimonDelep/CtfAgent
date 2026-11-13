import wave

# Ouvrir le fichier WAV et extraire les LSB
with wave.open('audio.wav', 'rb') as wav:
    frames = wav.readframes(wav.getnframes())
    
    # Extraire le LSB de chaque byte
    lsb_bits = []
    for byte in frames:
        lsb_bits.append(byte & 1)
    
    # Convertir les bits en bytes
    lsb_bytes = []
    for i in range(0, len(lsb_bits) - 7, 8):
        byte_val = 0
        for j in range(8):
            byte_val = (byte_val << 1) | lsb_bits[i + j]
        lsb_bytes.append(byte_val)
    
    # Afficher les premiers bytes en ASCII
    result = bytes(lsb_bytes[:200])
    print("LSB bytes (hex):", result[:50].hex())
    print("LSB bytes (ascii):", result)