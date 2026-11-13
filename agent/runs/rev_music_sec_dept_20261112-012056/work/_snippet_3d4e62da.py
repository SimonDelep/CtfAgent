with open('csirac/session.bin', 'rb') as f:
    data = f.read()

# Trouver la position de "flag{"
idx = data.find(b'\x81\x66\x81\x6c\x81\x61\x81\x67\x81\x7b')  # flag{
print(f"Position de flag{{: {idx}")

# Regardons les bytes autour de flag{
print("Bytes autour de flag{:")
for i in range(idx, min(idx+50, len(data))):
    print(f"  {i}: 0x{data[i]:02x} = {chr(data[i]) if 32 <= data[i] <= 126 else '?'}")