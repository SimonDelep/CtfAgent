with open('session.bin', 'rb') as f:
    data = f.read()

# Cherchons toutes les occurrences de 0x7b ('{') et 0x7d ('}')
print("Recherche de '{' (0x7b):")
for i, b in enumerate(data):
    if b == 0x7b:
        print(f"  Index {i}: 0x7b")
        # Afficher le contexte
        start = max(0, i-10)
        end = min(len(data), i+10)
        print(f"    Contexte: {data[start:end]}")

print("\nRecherche de '}' (0x7d):")
for i, b in enumerate(data):
    if b == 0x7d:
        print(f"  Index {i}: 0x7d")
        start = max(0, i-10)
        end = min(len(data), i+10)
        print(f"    Contexte: {data[start:end]}")
