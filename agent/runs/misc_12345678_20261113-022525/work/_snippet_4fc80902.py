import struct
import wave

with wave.open('audio.wav', 'rb') as wav:
    raw_data = wav.readframes(wav.getnframes())

samples = struct.unpack('<' + 'h' * (len(raw_data) // 2), raw_data)

# Extraire les valeurs positives entre 1 et 8
positive_sequence = [s for s in samples if 1 <= s <= 8]

# Peut-être que c'est un code où chaque valeur représente un bit
# et qu'on doit regrouper les bits pour former des octets

# Essayons: chaque valeur 1-8 représente 3 bits (0-7)
# Mais 8 = 1000, donc 4 bits...

# Autre idée: peut-être que c'est du base8 mais en utilisant les valeurs comme chiffres
# et qu'on doit convertir en texte ASCII

# Regardons si la séquence contient "csaw" en cherchant des patterns
# Peut-être que c'est un code où on doit lire les valeurs différemment

# Essayons de voir si c'est du Morse: 1-4 = point, 5-8 = trait
def to_morse(seq):
    morse = []
    for v in seq:
        if v <= 4:
            morse.append('.')
        else:
            morse.append('-')
    return ''.join(morse)

morse_seq = to_morse(positive_sequence[:100])
print(f"Morse (1-4=., 5-8=-): {morse_seq}")

# Décoder le Morse
morse_dict = {
    '.-': 'A', '-...': 'B', '-.-.': 'C', '-..': 'D', '.': 'E',
    '..-.': 'F', '--.': 'G', '....': 'H', '..': 'I', '.---': 'J',
    '-.-': 'K', '.-..': 'L', '--': 'M', '-.': 'N', '---': 'O',
    '.--.': 'P', '--.-': 'Q', '.-.': 'R', '...': 'S', '-': 'T',
    '..-': 'U', '...-': 'V', '.--': 'W', '-..-': 'X', '-.--': 'Y',
    '--..': 'Z'
}

# Essayer de décoder le Morse par groupes de 1-5 symboles
def decode_morse(morse_str):
    # Essayer de trouver des mots en découpant le morse
    result = []
    i = 0
    while i < len(morse_str):
        found = False
        for length in range(1, 6):
            if i + length <= len(morse_str):
                sub = morse_str[i:i+length]
                if sub in morse_dict:
                    result.append(morse_dict[sub])
                    i += length
                    found = True
                    break
        if not found:
            result.append('?')
            i += 1
    return ''.join(result)

print(f"Décodage Morse: {decode_morse(morse_seq)}")

# Autre idée: peut-être que c'est un code où chaque valeur représente
# une position dans l'alphabet, mais avec un décalage

# Essayons de trouver un décalage qui donne "csaw" ou "flag"
def try_all_shifts(seq):
    for shift in range(26):
        decoded = ''.join(chr(ord('a') + ((v - 1 + shift) % 26)) for v in seq[:50])
        if 'csaw' in decoded.lower() or 'flag' in decoded.lower():
            print(f"Shift {shift}: {decoded}")

try_all_shifts(positive_sequence)

# Peut-être que c'est un code où les valeurs 1-8 représentent des lettres A-H
# et qu'il faut appliquer une substitution monoalphabétique

# Regardons la fréquence des lettres dans le décodage A=1
from collections import Counter
decoded = ''.join(chr(ord('A') + v - 1) for v in positive_sequence)
letter_counts = Counter(decoded)
print(f"\nFréquence des lettres (A=1):")
for letter, count in letter_counts.most_common(10):
    print(f"  {letter}: {count}")