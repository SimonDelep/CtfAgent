with open('csirac/session.bin', 'rb') as f:
    data = f.read()

# La séquence après flag{ contient "s4lt26" répété
# Peut-être que c'est un XOR avec ce salt

# D'abord, trouvons où commence le vrai contenu du flag
# Après flag{, on a 0x81 0x0a (newline), puis des données

# Regardons la séquence hex complète après flag{
start = 134
end = start + 200
print("Hex dump:")
print(data[start:end].hex())

# Cherchons "s4lt26" en ASCII
salt = b"s4lt26"
idx = data.find(salt)
print(f"\nPosition de 's4lt26': {idx}")

# Si on trouve le salt, peut-être que le flag est XORé avec ce salt
# Regardons les bytes avant et après le salt
if idx != -1:
    print(f"\nBytes autour du salt:")
    print(data[idx-10:idx+30].hex())