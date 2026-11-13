import sqlite3

# Ouvrons une copie du DB pour voir le schéma
conn = sqlite3.connect('catalog.db')
cursor = conn.cursor()

# Liste des tables
cursor.execute("SELECT name FROM sqlite_master WHERE type='table';")
tables = cursor.fetchall()
print("Tables:", tables)

# Schéma de chaque table
for table in tables:
    table_name = table[0]
    cursor.execute(f"PRAGMA table_info({table_name});")
    cols = cursor.fetchall()
    print(f"\nTable {table_name}:")
    for col in cols:
        print(f"  {col}")

# Essayons de voir les données
for table in tables:
    table_name = table[0]
    cursor.execute(f"SELECT * FROM {table_name};")
    rows = cursor.fetchall()
    print(f"\nDonnées de {table_name}:")
    for row in rows:
        print(f"  {row}")

conn.close()