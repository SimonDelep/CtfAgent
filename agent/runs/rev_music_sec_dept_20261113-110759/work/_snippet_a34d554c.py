import struct

with open('csirac/session.bin', 'rb') as f:
    data = f.read()

# Décoder les séquences 0x81 XX en caractères ASCII
decoded = []
i = 0
while i < len(data):
    if data[i] == 0x81 and i + 1 < len(data):
        decoded.append(chr(data[i+1]))
        i += 2
    else:
        # Octet non encodé, on le garde en hex
        decoded.append(f'[{data[i]:02x}]')
        i += 1

result = ''.join(decoded)
print(result[:500])