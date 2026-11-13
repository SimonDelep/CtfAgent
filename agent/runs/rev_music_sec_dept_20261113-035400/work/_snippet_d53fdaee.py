with open('session.bin', 'rb') as f:
    data = f.read()

# Pattern: 0x81 suivi d'un caractère ASCII imprimable
# On va extraire tous les octets après 0x81 qui sont des caractères ASCII
result = []
i = 0
while i < len(data):
    if data[i] == 0x81 and i + 1 < len(data):
        next_byte = data[i + 1]
        if 32 <= next_byte <= 126:  # ASCII imprimable
            result.append(chr(next_byte))
            i += 2
            continue
    # Sinon, on peut aussi garder certains octets non-ASCII pour analyse
    i += 1

print(''.join(result))