with open('csirac/session.bin', 'rb') as f:
    data = f.read()

# Regardons la séquence complète après flag{
# On voit 0x81 0x0a (newline), puis 0x02 0x00 0x00 0x00 0x36...
# Peut-être que 0x81 est un préfixe pour les caractères ASCII

# Essayons de décoder en ignorant les bytes 0x81 et en regardant ce qui suit
start = 134
end = 182
segment = data[start:end]

print("Segment à décoder:")
for i, b in enumerate(segment):
    if b == 0x81:
        print(f"  {i}: 0x81 (préfixe)")
    else:
        print(f"  {i}: 0x{b:02x} = {chr(b) if 32 <= b <= 126 else '?'}")

# Peut-être que le flag est encodé avec un XOR différent
# Regardons les bytes qui ne sont pas 0x81
non_81 = [b for b in segment if b != 0x81]
print(f"\nBytes non-0x81: {bytes(non_81).hex()}")