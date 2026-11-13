with open('csirac/session.bin', 'rb') as f:
    data = f.read()

# Chercher le motif 0x81 suivi d'un caractère
# Le flag semble être encodé avec 0x81 comme préfixe
result = []
i = 0
while i < len(data) - 1:
    if data[i] == 0x81:
        result.append(chr(data[i+1]))
        i += 2
    else:
        i += 1

print("Décodage avec motif 0x81:")
print(''.join(result[:100]))

# Chercher où commence vraiment le flag
# On voit dans le dump qu'il y a "flag{" quelque part
# Regardons les bytes autour de l'offset 124 mentionné dans le mémoire
print("\nBytes autour de l'offset 124:")
for i in range(120, 150):
    if i < len(data):
        b = data[i]
        if 32 <= b < 127:
            print(f"{i}: {chr(b)} ({b:02x})")
        else:
            print(f"{i}: {b:02x}")
