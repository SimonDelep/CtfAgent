import wave
import struct
from collections import Counter

with wave.open('audio.wav', 'rb') as wav:
    frames = wav.readframes(wav.getnframes())
    samples = struct.unpack('<' + 'h' * (len(frames) // 2), frames)
    right = samples[1::2]
    
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
    
    seqs = find_silence_sequences(right, 100)
    seqs = seqs[1:]
    
    # Identifier les séparateurs (valeurs >= 50)
    groups = []
    current_group = []
    for s in seqs:
        if s >= 50:
            if current_group:
                groups.append(current_group)
                current_group = []
        else:
            current_group.append(s)
    if current_group:
        groups.append(current_group)
    
    # Pour chaque groupe, extraire les valeurs non-1 et les convertir en Morse
    # Hypothèse: 2-3 = point (.), 4-6 = trait (-)
    # Les valeurs 7+ pourraient être des séparateurs entre lettres
    
    def group_to_morse(group):
        # Extraire les valeurs non-1
        non_ones = [v for v in group if v != 1]
        # Convertir en Morse
        morse = []
        for v in non_ones:
            if v <= 3:
                morse.append('.')
            elif v <= 6:
                morse.append('-')
            else:
                # Valeur >= 7, peut-être séparateur
                morse.append(' ')
        return ''.join(morse)
    
    # Afficher les premiers groupes convertis
    print("Conversion des premiers groupes en Morse:")
    for i, g in enumerate(groups[:10]):
        morse = group_to_morse(g)
        print(f"Group {i}: {morse[:50]}")
    
    # Essayer de décoder le Morse
    morse_dict = {
        '.-': 'A', '-...': 'B', '-.-.': 'C', '-..': 'D', '.': 'E',
        '..-.': 'F', '--.': 'G', '....': 'H', '..': 'I', '.---': 'J',
        '-.-': 'K', '.-..': 'L', '--': 'M', '-.': 'N', '---': 'O',
        '.--.': 'P', '--.-': 'Q', '.-.': 'R', '...': 'S', '-': 'T',
        '..-': 'U', '...-': 'V', '.--': 'W', '-..-': 'X', '-.--': 'Y',
        '--..': 'Z', '-----': '0', '.----': '1', '..---': '2', '...--': '3',
        '....-': '4', '.....': '5', '-....': '6', '--...': '7', '---..': '8',
        '----.': '9'
    }
    
    # Essayer de décoder chaque groupe
    print("\nDécodage des groupes:")
    for i, g in enumerate(groups[:10]):
        morse = group_to_morse(g)
        # Séparer par espaces
        letters = morse.split(' ')
        decoded = []
        for l in letters:
            if l:
                decoded.append(morse_dict.get(l, '?'))
        print(f"Group {i}: {''.join(decoded)}")