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
print("Texte complet extrait:")
print(text)
print("\n---")
print("Longueur:", len(text))

# Cherchons 'flag{' et tout ce qui suit
if 'flag{' in text:
    idx = text.index('flag{')
    print(f"\nÀ partir de 'flag{{':")
    print(text[idx:])
