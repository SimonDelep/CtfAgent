import sqlite3

# Copions le DB et WAL pour inspection
import shutil
shutil.copy('catalog.db', 'catalog_copy.db')
shutil.copy('catalog.db-wal', 'catalog_copy.db-wal')

# Ouvrons avec le WAL
conn = sqlite3.connect('catalog_copy.db')
conn.execute("PRAGMA wal_checkpoint(PASSIVE);")  # Essayons de checkpoint
cursor = conn.cursor()

# Liste des tables
cursor.execute("SELECT name FROM sqlite_master WHERE type='table';")
tables = cursor.fetchall()
print("Tables:", tables)

# Schéma
for table in tables:
    table_name = table[0]
    cursor.execute(f"PRAGMA table_info({table_name});")
    cols = cursor.fetchall()
    print(f"\nTable {table_name}:")
    for col in cols:
        print(f"  {col}")

# Données
for table in tables:
    table_name = table[0]
    cursor.execute(f"SELECT * FROM {table_name};")
    rows = cursor.fetchall()
    print(f"\nDonnées de {table_name}:")
    for row in rows:
        if len(row) > 1 and isinstance(row[1], bytes):
            print(f"  id={row[0]}, share={row[1].hex()}")
        else:
            print(f"  {row}")

conn.close()