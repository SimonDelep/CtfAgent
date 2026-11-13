# Récupérer les singletons et les convertir en ASCII
singletons = [50913, 50517, 50915, 50894, 50969, 50581, 50957, 50698, 50142, 50207]

# Essayons modulo 256
for p in singletons:
    print(f"{p} -> {p % 256} -> {chr(p % 256) if 32 <= p % 256 < 127 else '?'}")