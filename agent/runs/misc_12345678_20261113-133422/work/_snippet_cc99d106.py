import wave
import struct

with wave.open('audio.wav', 'rb') as wav:
    data = wav.readframes(wav.getnframes())
    samples = struct.unpack('<' + 'h' * (len(data) // 2), data)
    
    # Peut-être que le message est dans les valeurs absolues modulo quelque chose
    # Ou peut-être que les valeurs positives et négatives ont un sens différent
    
    # Regardons si les valeurs peuvent être interprétées comme des codes ASCII décalés
    # Essayons de voir si les valeurs absolues forment un message
    
    abs_samples = [abs(s) for s in samples]
    
    # Filtrer les valeurs qui pourraient être des caractères ASCII
    # Peut-être que les valeurs > 0 sont significatives
    message = []
    for s in samples:
        if s != 0:
            # Essayer de mapper les valeurs à des caractères
            # Les valeurs sont entre 1 et 32767
            # Peut-être que les petites valeurs sont des caractères
            if 1 <= abs(s) <= 127:
                message.append(chr(abs(s)))
    
    print("Message avec valeurs non nulles (1-127):", ''.join(message)[:200])
    print(f"Longueur: {len(message)}")