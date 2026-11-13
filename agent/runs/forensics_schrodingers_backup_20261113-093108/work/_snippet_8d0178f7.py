import sqlite3
import shutil

# Copier le WAL et la base pour les examiner
shutil.copy('catalog.db', 'catalog_copy.db')
shutil.copy('catalog.db-wal', 'catalog_copy.db-wal')

# Ouvrir la copie
conn = sqlite3.connect('catalog_copy.db')
cursor = conn.cursor()

# Lister les tables
cursor.execute("SELECT name FROM sqlite_master WHERE type='table';")
tables = cursor.fetchall()
print("Tables:", tables)

# Pour chaque table, montrer le schéma
for table in tables:
    table_name = table[0]
    cursor.execute(f"PRAGMA table_info({table_name});")
    columns = cursor.fetchall()
    print(f"\nTable {table_name}:")
    for col in columns:
        print(f"  {col}")
    
    # Essayer de sélectionner les données
    try:
        cursor.execute(f"SELECT * FROM {table_name};")
        rows = cursor.fetchall()
        print(f"  Données ({len(rows)} lignes):")
        for row in rows[:5]:
            print(f"    {row}")
    except Exception as e:
        print(f"  Erreur: {e}")

conn.close()