# Lisons le WAL pour voir sa structure
with open('catalog.db-wal', 'rb') as f:
    data = f.read()

print(f"Taille du WAL: {len(data)} bytes")
print(f"Premiers 100 bytes (hex): {data[:100].hex()}")
print(f"Derniers 100 bytes (hex): {data[-100:].hex()}")