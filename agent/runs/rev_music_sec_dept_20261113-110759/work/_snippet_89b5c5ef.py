with open('csirac/session.bin', 'rb') as f:
    data = f.read()

# Trouver la position de "flag{" encodé
# 81 66 81 6c 81 61 81 67 81 7b = flag{
flag_start = data.find(bytes([0x81, 0x66, 0x81, 0x6c, 0x81, 0x61, 0x81, 0x67, 0x81, 0x7b]))
print(f"flag{ position: {flag_start}")

# Après flag{, il y a 0x81 0x0a = '\n', puis 02 00 00 00
after_flag = data[flag_start + 10:]  # après le '{'
print(f"Après flag{{: {after_flag[:30].hex()}")

# Chercher le motif s4lt26 (73 34 6c 74 32 36)
s4lt26_pos = data.find(b's4lt26')
print(f"s4lt26 position: {s4lt26_pos}")
print(f"Contexte autour de s4lt26: {data[s4lt26_pos-20:s4lt26_pos+50].hex()}")