with open('csirac/session.bin', 'rb') as f:
    data = f.read()

# Le flag commence après "flag{\n" qui est à l'offset 124-135
# Offset 136 est le début du contenu chiffré
# Offset 182 est le début de "s4lt26"

encrypted_start = 136
encrypted_end = 182  # où commence s4lt26

print("Données chiffrées (offset 136 à 181):")
encrypted = data[encrypted_start:encrypted_end]
print("Longueur:", len(encrypted))
print("Hex:", encrypted.hex())

# Le salt est "s4lt26" répété
salt = b"s4lt26"
print("\nSalt:", salt)

# Essayons XOR avec le salt
decrypted = []
for i, b in enumerate(encrypted):
    decrypted.append(b ^ salt[i % len(salt)])

print("\nXOR avec s4lt26:")
print(bytes(decrypted))

# Essayons aussi de voir si c'est un XOR avec une clé dérivée du salt
# Peut-être que le salt est utilisé différemment
