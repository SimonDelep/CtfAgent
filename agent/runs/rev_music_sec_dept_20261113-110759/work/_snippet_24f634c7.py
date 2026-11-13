# Chercher "flag{" dans le fichier décodé
with open('session.bin', 'rb') as f:
    data = f.read()

# Trouver la position de "flag{"
# D'abord, trouver où "flag{" apparaît en cherchant les paires 0x81
flag_start = None
for i in range(len(data)-8):
    if data[i:i+10] == bytes([0x81, 0x66, 0x81, 0x6c, 0x81, 0x61, 0x81, 0x67, 0x81, 0x7b]):
        flag_start = i
        break

print(f"Position de 'flag{{': {flag_start}")

if flag_start:
    # Afficher les octets autour de flag{
    print("\nOctets autour de 'flag{':")
    print(data[flag_start:flag_start+50].hex())
    
    # Le flag semble être encodé après "flag{"
    # Regardons ce qui suit
    print("\nAprès 'flag{':")
    after_flag = data[flag_start+10:flag_start+100]
    print(after_flag.hex())
    
    # Décoder ce qui suit
    i = flag_start + 10
    decoded_flag = []
    while i < len(data) and len(decoded_flag) < 50:
        if data[i] == 0x81 and i+1 < len(data):
            val = data[i+1]
            if 32 <= val < 127:
                decoded_flag.append(chr(val))
            else:
                decoded_flag.append(f'[{val:02x}]')
            i += 2
        elif data[i] == 0x80 and i+1 < len(data):
            val = data[i+1]
            if 32 <= val < 127:
                decoded_flag.append(chr(val))
            else:
                decoded_flag.append(f'<{val:02x}>')
            i += 2
        else:
            if data[i] >= 32 and data[i] < 127:
                decoded_flag.append(chr(data[i]))
            else:
                decoded_flag.append(f'.{data[i]:02x}.')
            i += 1
    
    print("\nFlag décodé (partiel):")
    print(''.join(decoded_flag))