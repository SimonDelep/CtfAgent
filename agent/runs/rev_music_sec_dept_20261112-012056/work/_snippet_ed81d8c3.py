with open('csirac/session.bin', 'rb') as f:
    data = f.read()

# Extraire tous les caractères après 0x81
decoded = []
i = 0
while i < len(data):
    if data[i] == 0x81 and i+1 < len(data):
        decoded.append(chr(data[i+1]))
        i += 2
    else:
        i += 1

result = ''.join(decoded)
print(result)