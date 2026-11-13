import sqlite3

conn = sqlite3.connect('catalog.db')
cursor = conn.cursor()

# Extraire les données de north
cursor.execute("SELECT id, share FROM north;")
north_rows = cursor.fetchall()
print("Table north:")
for row in north_rows:
    print(f"  id={row[0]}, share={row[1]!r} (len={len(row[1]) if row[1] else 0})")

# Extraire les données de south
cursor.execute("SELECT id, share FROM south;")
south_rows = cursor.fetchall()
print("\nTable south:")
for row in south_rows:
    print(f"  id={row[0]}, share={row[1]!r} (len={len(row[1]) if row[1] else 0})")

# Extraire les données de control
cursor.execute("SELECT * FROM control;")
control_rows = cursor.fetchall()
print("\nTable control:")
for row in control_rows:
    print(f"  {row}")

# Extraire les données de maintenance
cursor.execute("SELECT * FROM maintenance;")
maintenance_rows = cursor.fetchall()
print("\nTable maintenance:")
for row in maintenance_rows:
    print(f"  {row}")

conn.close()