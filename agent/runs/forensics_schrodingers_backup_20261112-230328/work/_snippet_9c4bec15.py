import sqlite3

# Ouvrir une copie de travail
conn = sqlite3.connect('catalog.db')
cursor = conn.cursor()

# Lister les tables
cursor.execute("SELECT name FROM sqlite_master WHERE type='table';")
tables = cursor.fetchall()
print("Tables:", tables)

# Pour chaque table, voir la structure
for table in tables:
    tname = table[0]
    cursor.execute(f"PRAGMA table_info({tname});")
    cols = cursor.fetchall()
    print(f"\nTable {tname}:")
    for col in cols:
        print(f"  {col}")