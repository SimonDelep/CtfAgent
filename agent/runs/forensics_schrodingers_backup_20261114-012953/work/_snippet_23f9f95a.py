import sqlite3

conn = sqlite3.connect("catalog_work.db", isolation_level=None)

# Lire le contenu actuel
print("=== control ===")
for row in conn.execute("SELECT * FROM control"):
    print(row)

print("\n=== north ===")
for row in conn.execute("SELECT * FROM north"):
    print(row)

print("\n=== south ===")
for row in conn.execute("SELECT * FROM south"):
    print(row)

print("\n=== maintenance ===")
for row in conn.execute("SELECT * FROM maintenance"):
    print(row)

conn.close()