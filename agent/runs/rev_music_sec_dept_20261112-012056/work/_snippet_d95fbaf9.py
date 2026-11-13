with open('csirac/session.bin', 'rb') as f:
    data = f.read()

# Trouver la position de "flag{"
flag_start = data.find(b'flag{')
print("flag{ found at offset:", flag_start)

# Trouver la position de "s4lt26"
salt_pos = data.find(b's4lt26')
print("s4lt26 found at offset:", salt_pos)

# Afficher les bytes autour de flag{
print("\nBytes around flag{:")
for i in range(flag_start, min(flag_start + 60, len(data))):
    b = data[i]
    if 32 <= b < 127:
        print(f"{i}: {chr(b)} ({b:02x})")
    else:
        print(f"{i}: {b:02x}")

# Afficher les bytes autour de s4lt26
print("\nBytes around s4lt26:")
for i in range(salt_pos, min(salt_pos + 40, len(data))):
    b = data[i]
    if 32 <= b < 127:
        print(f"{i}: {chr(b)} ({b:02x})")
    else:
        print(f"{i}: {b:02x}")
