with open('session.bin', 'rb') as f:
    data = f.read()

# Trouver le début de "flag{" avec le motif 0x81
target = bytes([0x81, 0x66, 0x81, 0x6c, 0x81, 0x61, 0x81, 0x67, 0x81, 0x7b])
idx = data.find(target)
print(f"Index de 'flag{{': {idx}")

if idx >= 0:
    # Extraire le flag complet
    result = []
    i = idx
    while i < len(data):
        if data[i] == 0x81 and i+1 < len(data):
            c = data[i+1]
            if 32 <= c < 127:  # Caractère ASCII imprimable
                result.append(chr(c))
                i += 2
            else:
                # Caractère non-imprimable, peut-être la fin
                i += 2
                if c == 0x0a:  # newline
                    break
                if c == 0x00:
                    break
        else:
            i += 1
    
    flag = ''.join(result)
    print("Flag extrait:", flag)
    
    # Trouver la première occurrence de '}'
    if '}' in flag:
        end_idx = flag.index('}')
        print("Flag final:", flag[:end_idx+1])
