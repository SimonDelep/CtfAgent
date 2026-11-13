import sqlite3
import shutil

# Copier la base de données pour éviter de modifier l'originale
shutil.copy('catalog.db', 'catalog_copy.db')

# Ouvrir la copie
conn = sqlite3.connect('catalog_copy.db')
cursor = conn.cursor()

# Lister les tables
cursor.execute("SELECT name FROM sqlite_master WHERE type='table';")
tables = cursor.fetchall()
print("Tables:", tables)

# Pour chaque table, afficher le schéma
for table in tables:
    table_name = table[0]
    print(f"\n=== Table: {table_name} ===")
    cursor.execute(f"PRAGMA table_info({table_name});")
    columns = cursor.fetchall()
    for col in columns:
        print(f"  {col}")
    
    # Afficher quelques lignes
    cursor.execute(f"SELECT * FROM {table_name} LIMIT 5;")
    rows = cursor.fetchall()
    print(f"  Données (max 5 lignes):")
    for row in rows:
        print(f"    {row}")

conn.close()
