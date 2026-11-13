# Ports fréquents (hors 9000 qui est le port de destination standard)
frequent_ports = [40052, 40100, 40104, 40111, 40115, 40119]

# Valeurs mod 256
print("Ports fréquents mod 256:")
for p in frequent_ports:
    print(f"  {p} -> {p % 256} -> {chr(p % 256) if 32 <= p % 256 < 127 else '?'}")

# Peut-être que la clé est la séquence de ces ports dans l'ordre d'apparition
# Ou peut-être que chaque singleton est XORé avec un port fréquent correspondant

# Regardons les singletons mod 256
singletons_mod256 = [p % 256 for p in [50913, 50517, 50915, 50894, 50969, 50581, 50957, 50698, 50142, 50207, 50046, 50573, 50272, 50129, 50784, 50716, 50856, 50695, 50947, 50275]]
print(f"\nSingletons mod 256 (premiers 20): {singletons_mod256}")

# Si on XOR avec une clé, on devrait obtenir des caractères ASCII lisibles
# Essayons de deviner la clé

# Peut-être que le flag commence par "csaw{"
# Si le premier singleton XOR clé = 'c' (99), alors clé = singleton XOR 99
print("\nSi le flag commence par 'csaw{':")
target = b'csaw{'
for i, s in enumerate(singletons_mod256[:5]):
    key_byte = s ^ target[i]
    print(f"  singleton[{i}]={s} XOR key={key_byte} = {chr(key_byte)} (target '{chr(target[i])}')")
