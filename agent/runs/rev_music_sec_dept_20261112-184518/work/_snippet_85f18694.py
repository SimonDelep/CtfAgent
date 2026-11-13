with open('session.bin', 'rb') as f:
    data = f.read()

# Chercher le flag encodé avec 0x81 prefix
# À partir de 0x7c, on voit: 81 66 81 6c 81 61 81 67 81 7b
# C'est 'f' 'l' 'a' 'g' '{'

# Extraire le flag en décodant le format 0x81 + char
flag_start = 0x7c
flag_bytes = []
i = flag_start
while i < len(data):
    if data[i] == 0x81 and i+1 < len(data):
        flag_bytes.append(data[i+1])
        i += 2
    elif data[i] == 0x81 and i+1 >= len(data):
        break
    else:
        # On a atteint la fin du flag
        break

print("Flag extrait:", bytes(flag_bytes).decode('latin-1'))