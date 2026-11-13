import wave
import struct

with wave.open('audio.wav', 'rb') as wav:
    data = wav.readframes(wav.getnframes())
    samples = struct.unpack('<' + 'h' * (len(data) // 2), data)
    
    # Essayer de voir si les valeurs absolues forment des caractères
    # Les valeurs sont entre -32768 et 32767
    # Peut-être que les valeurs positives ou négatives ont un sens
    
    # Regardons les valeurs uniques et leur fréquence
    from collections import Counter
    counts = Counter(samples)
    print("Valeurs les plus fréquentes:")
    for val, cnt in counts.most_common(20):
        print(f"  {val}: {cnt}")
    
    # Regardons si les valeurs peuvent être des ASCII
    # Peut-être que certaines valeurs correspondent à des caractères imprimables
    ascii_chars = []
    for i, s in enumerate(samples):
        if 32 <= s <= 126:
            ascii_chars.append((i, s, chr(s)))
    
    print(f"\nÉchantillons dans la plage ASCII imprimable (32-126): {len(ascii_chars)}")
    if ascii_chars:
        print("Premiers 50:", ascii_chars[:50])