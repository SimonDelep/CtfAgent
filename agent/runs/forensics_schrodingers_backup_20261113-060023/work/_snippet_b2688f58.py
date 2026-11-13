import sqlite3

conn = sqlite3.connect('catalog.db')
cursor = conn.cursor()

print("=== NORTH ===")
cursor.execute("SELECT id, share FROM north")
for row in cursor.fetchall():
    print(f"id={row[0]}, share={row[1].hex() if row[1] else 'NULL'}")

print("\n=== SOUTH ===")
cursor.execute("SELECT id, share FROM south")
for row in cursor.fetchall():
    print(f"id={row[0]}, share={row[1].hex() if row[1] else 'NULL'}")

print("\n=== CONTROL ===")
cursor.execute("SELECT * FROM control")
for row in cursor.fetchall():
    print(row)

conn.close()