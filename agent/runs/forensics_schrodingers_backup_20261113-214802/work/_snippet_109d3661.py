import sqlite3

# Ouvrir catalog.db pour voir le schéma
conn = sqlite3.connect('catalog.db')
cursor = conn.cursor()

# Lister les tables
cursor.execute("SELECT name FROM sqlite_master WHERE type='table';")
tables = cursor.fetchall()
print("Tables:", tables)

# Pour chaque table, voir le schéma
for table in tables:
    tname = table[0]
    cursor.execute(f"PRAGMA table_info({tname});")
    cols = cursor.fetchall()
    print(f"\nTable {tname}:")
    for col in cols:
        print(f"  {col}")

# Voir les données actuelles dans les tables
for table in tables:
    tname = table[0]
    cursor.execute(f"SELECT * FROM {tname} LIMIT 5;")
    rows = cursor.fetchall()
    print(f"\nDonnées dans {tname} (max 5):")
    for row in rows:
        print(f"  {row}")

conn.close()