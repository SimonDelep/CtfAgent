# Analysons les ports singletons et fréquents
singletons = [50913, 50517, 50915, 50894, 50969, 50581, 50957, 50698, 50142, 50207, 50046, 50573, 50272, 50129, 50784, 50716, 50856, 50695, 50947, 50275]

# Regardons les ports en binaire ou en décomposition
print("Singleton ports analysis:")
for i, port in enumerate(singletons[:20]):
    print(f"  {i}: {port} = 0x{port:04x} = bytes: {port.to_bytes(2, 'big').hex()}")

# Les ports fréquents
frequent = [40115, 40104, 40052, 40100, 40111, 40119]
print("\nFrequent ports:")
for port in frequent:
    print(f"  {port} = 0x{port:04x}")

# Peut-être que les ports singletons encodent des bits ou des octets
# Regardons les différences entre ports singletons
print("\nDifferences between consecutive singletons:")
for i in range(1, len(singletons)):
    diff = singletons[i] - singletons[i-1]
    print(f"  {singletons[i]} - {singletons[i-1]} = {diff}")