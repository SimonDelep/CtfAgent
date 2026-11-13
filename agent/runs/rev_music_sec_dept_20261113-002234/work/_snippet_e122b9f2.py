# Analyser session.bin pour trouver le flag
with open('csirac/session.bin', 'rb') as f:
    data = f.read()

# Chercher la séquence "flag{" encodée (0x81 0x66, 0x81 0x6c, 0x81 0x61, 0x81 0x67, 0x81 0x7b)
# Et extraire ce qui suit jusqu'à la fermeture

# D'abord, trouvons où commence "flag{"
flag_start = None
i = 0
while i < len(data) - 9:
    if data[i:i+10] == bytes([0x81, 0x66, 0x81, 0x6c, 0x81, 0x61, 0x81, 0x67, 0x81, 0x7b]):
        flag_start = i
        break
    i += 1

print("flag{ trouvé à la position", flag_start)

if flag_start:
    # Extraire tout après "flag{"
    after_flag = data[flag_start + 10:]  # Après les 10 octets de "flag{"
    
    # Chercher la fermeture "}" (0x81 0x7d)
    close_pos = after_flag.find(bytes([0x81, 0x7d]))
    if close_pos != -1:
        flag_content = after_flag[:close_pos]
        print("Contenu du flag (brut):", flag_content)
        print("Longueur:", len(flag_content))
        
        # Essayer de décoder en remplaçant 0x81XX par le caractère
        decoded_flag = bytearray()
        i = 0
        while i < len(flag_content):
            if flag_content[i] == 0x81 and i + 1 < len(flag_content):
                decoded_flag.append(flag_content[i+1])
                i += 2
            else:
                decoded_flag.append(flag_content[i])
                i += 1
        print("Flag decode:", decoded_flag.decode('latin-1', errors='replace'))
    else:
        print("Pas de } trouve")
        print("Suite apres flag{:", after_flag[:100])