import sqlite3
import os

# Copier le WAL et DB pour éviter checkpoint
os.system("cp catalog.db catalog_work.db")
os.system("cp catalog.db-wal catalog_work.db-wal")

# Ouvrir avec mode RO et nocheckpointer
conn = sqlite3.connect("catalog_work.db", isolation_level=None)
conn.execute("PRAGMA journal_mode=WAL")

# Lire le schéma
cursor = conn.execute("SELECT name FROM sqlite_master WHERE type='table'")
tables = cursor.fetchall()
print("Tables:", tables)

# Pour chaque table, voir le contenu
for (table_name,) in tables:
    cursor = conn.execute(f"SELECT COUNT(*) FROM {table_name}")
    count = cursor.fetchone()[0]
    print(f"Table {table_name}: {count} rows")
    
    # Afficher les colonnes
    cursor = conn.execute(f"PRAGMA table_info({table_name})")
    cols = cursor.fetchall()
    print(f"  Columns: {cols}")

conn.close()