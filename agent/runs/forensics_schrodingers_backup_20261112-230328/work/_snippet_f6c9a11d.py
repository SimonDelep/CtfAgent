import sqlite3

conn = sqlite3.connect('catalog.db')
cursor = conn.cursor()

print("=== Table control ===")
cursor.execute("SELECT * FROM control;")
for row in cursor.fetchall():
    print(row)

print("\n=== Table north ===")
cursor.execute("SELECT * FROM north;")
for row in cursor.fetchall():
    print(row)

print("\n=== Table south ===")
cursor.execute("SELECT * FROM south;")
for row in cursor.fetchall():
    print(row)

print("\n=== Table maintenance ===")
cursor.execute("SELECT * FROM maintenance;")
for row in cursor.fetchall():
    print(row)