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

# Essayer de mapper les longueurs à des valeurs Morse
# Hypothèse: longueur / 6 arrondi = durée en unités
# 6 -> 1 (point), 18 -> 3 (trait)
# Mais nous avons 6, 7, 8, 9, 10, 11, 12, ...

# Peut-être que c'est plus simple : 6-8 = point, 9-12 = trait, >12 = séparateur
def length_to_morse(l):
    if 6 <= l <= 8:
        return '.'
    elif 9 <= l <= 12:
        return '-'
    else:
        return ' '  # séparateur

morse_chars = [length_to_morse(l) for l in lengths]
morse_str = ''.join(morse_chars)
print(f"Chaine Morse: {morse_str[:100]}")

# Décoder Morse
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

# Décoder la chaine Morse
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

decoded = decode_morse(morse_str)
print(f"Décodé: {decoded[:50]}")

# Essayons d'autres mappings
print("\n--- Essayons 6-7 = point, 8-10 = trait ---")
def length_to_morse2(l):
    if 6 <= l <= 7:
        return '.'
    elif 8 <= l <= 10:
        return '-'
    else:
        return ' '

morse_chars2 = [length_to_morse2(l) for l in lengths]
morse_str2 = ''.join(morse_chars2)
print(f"Chaine Morse: {morse_str2[:100]}")
decoded2 = decode_morse(morse_str2)
print(f"Décodé: {decoded2[:50]}")