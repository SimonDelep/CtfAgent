with open('session.bin', 'rb') as f:
    data = f.read()

# Le motif semble être: chaque caractère ASCII est précédé par 0x81
# Ou peut-être que 0x81 est un séparateur
# Regardons les octets autour de "flag{"

# Cherchons la séquence qui correspond à "flag{"
# f=0x66, l=0x6c, a=0x61, g=0x67, {=0x7b

# Si chaque caractère est précédé par 0x81, alors on devrait voir:
# 81 66 81 6c 81 61 81 67 81 7b

# Trouvons cette séquence
target = bytes([0x81, 0x66, 0x81, 0x6c, 0x81, 0x61, 0x81, 0x67, 0x81, 0x7b])
idx = data.find(target)
print(f"Index de 'flag{{' avec 0x81: {idx}")

if idx >= 0:
    # Extraire le flag en sautant les 0x81
    flag_start = idx
    # On va lire jusqu'à ce qu'on trouve une séquence qui ne correspond pas au motif
    result = []
    i = idx
    while i < len(data):
        if data[i] == 0x81 and i+1 < len(data):
            result.append(chr(data[i+1]))
            i += 2
        else:
            break
    print("Flag extrait:", ''.join(result))
else:
    # Essayons une approche différente: extraire tous les octets pairs (ou impairs)
    # Regardons la structure
    print("Recherche alternative...")
    # Peut-être que 0x81 est un préfixe pour chaque caractère
    # Extraire tous les octets qui ne sont pas 0x81
    chars = [chr(b) for b in data if b != 0x81 and 32 <= b < 127]
    print("Caractères ASCII non-0x81:", ''.join(chars[:200]))
