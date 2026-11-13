import wave
import struct

# Ouvrir le fichier WAV
with wave.open('audio.wav', 'rb') as wf:
    data = wf.readframes(wf.getnframes())
    
# Convertir en échantillons
samples = struct.unpack('<' + 'h' * (len(data) // 2), data)

# Trouver toutes les séquences de zéros avec min_len=6
def find_zero_sequences(samples, min_len=6):
    sequences = []
    current_len = 0
    current_start = 0
    for i, s in enumerate(samples):
        if s == 0:
            if current_len == 0:
                current_start = i
            current_len += 1
        else:
            if current_len >= min_len:
                sequences.append((current_start, current_len))
            current_len = 0
    if current_len >= min_len:
        sequences.append((current_start, current_len))
    return sequences

all_zeros = find_zero_sequences(samples, min_len=6)
lengths = [l for _, l in all_zeros]

# Afficher les longueurs uniques et leurs positions
from collections import Counter
counts = Counter(lengths)
print("Longueurs et comptages:")
for l, c in sorted(counts.items()):
    print(f"  {l}: {c}")

# Trouver la longueur minimale et maximale
print(f"\nLongueur min: {min(lengths)}, max: {max(lengths)}")

# Peut-être que c'est basé sur la médiane ou la moyenne
print(f"Médiane: {sorted(lengths)[len(lengths)//2]}")
print(f"Moyenne: {sum(lengths)/len(lengths):.2f}")

# Essayons de trouver un seuil qui sépare point/trait
# Si on suppose que c'est du Morse, on devrait avoir environ 2x plus de points que de traits
# ou une distribution spécifique

# Essayons différents seuils et voyons lequel donne le plus de lettres valides
morse_code = {
    '.-': 'A', '-...': 'B', '-.-.': 'C', '-..': 'D', '.': 'E',
    '..-.': 'F', '--.': 'G', '....': 'H', '..': 'I', '.---': 'J',
    '-.-': 'K', '.-..': 'L', '--': 'M', '-.': 'N', '---': 'O',
    '.--.': 'P', '--.-': 'Q', '.-.': 'R', '...': 'S', '-': 'T',
    '..-': 'U', '...-': 'V', '.--': 'W', '-..-': 'X', '-.--': 'Y',
    '--..': 'Z', '-----': '0', '.----': '1', '..---': '2', '...--': '3',
    '....-': '4', '.....': '5', '-....': '6', '--...': '7', '---..': '8',
    '----.': '9'
}

def decode_morse(morse_str):
    result = []
    current = ''
    for c in morse_str:
        if c == ' ':
            if current:
                result.append(morse_code.get(current, '?'))
                current = ''
        else:
            current += c
    if current:
        result.append(morse_code.get(current, '?'))
    return ''.join(result)

# Tester différents seuils
for threshold in range(6, 15):
    def length_to_morse(l, t=threshold):
        if l < t:
            return '.'
        elif l > t + 3:
            return ' '  # séparateur
        else:
            return '-'
    
    morse_chars = [length_to_morse(l) for l in lengths]
    morse_str = ''.join(morse_chars)
    decoded = decode_morse(morse_str)
    
    # Compter les lettres valides (A-Z, 0-9)
    valid_count = sum(1 for c in decoded if c.isalnum())
    print(f"Seuil {threshold}: valid={valid_count}, decoded={decoded[:30]}")