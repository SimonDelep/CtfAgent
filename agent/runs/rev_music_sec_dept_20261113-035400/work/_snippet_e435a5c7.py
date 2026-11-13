with open('session.bin', 'rb') as f:
    data = f.read()

# Extraire tous les caractères qui suivent 0x81
result = []
for i in range(len(data)-1):
    if data[i] == 0x81:
        c = data[i+1]
        if 32 <= c < 127:
            result.append(chr(c))

text = ''.join(result)
print("Texte extrait (tous les caractères après 0x81):")
print(text[:500])
print("...")
print(text[500:1000])

# Cherchons 'flag{' dans ce texte
if 'flag{' in text:
    idx = text.index('flag{')
    print(f"\nFlag trouvé à l'index {idx}")
    # Trouver la fin du flag (premier '}' après 'flag{')
    end_idx = text.index('}', idx)
    print("Flag:", text[idx:end_idx+1])
