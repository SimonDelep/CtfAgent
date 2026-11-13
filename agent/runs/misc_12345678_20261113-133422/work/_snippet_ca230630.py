import wave
import struct

with wave.open('audio.wav', 'rb') as wav:
    data = wav.readframes(wav.getnframes())
    samples = struct.unpack('<' + 'h' * (len(data) // 2), data)
    
    # Extraire les échantillons dans la plage ASCII imprimable
    message = []
    for i, s in enumerate(samples):
        if 32 <= s <= 126:
            message.append(chr(s))
    
    print("Message extrait:", ''.join(message)[:500])
    print(f"Longueur: {len(message)}")