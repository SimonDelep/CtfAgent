import sqlite3

# Ouvrir la base de données (copie pour éviter d'altérer le WAL)
conn = sqlite3.connect('catalog_copy.db')
cursor = conn.cursor()

# Lister les tables
cursor.execute("SELECT name FROM sqlite_master WHERE type='table';")
tables = cursor.fetchall()
print("Tables:", tables)

# Pour chaque table, montrer la structure
for table in tables:
    table_name = table[0]
    print(f"\n--- Table: {table_name} ---")
    cursor.execute(f"PRAGMA table_info({table_name});")
    columns = cursor.fetchall()
    for col in columns:
        print(f"  {col}")
    
    # Afficher quelques lignes
    cursor.execute(f"SELECT * FROM {table_name} LIMIT 5;")
    rows = cursor.fetchall()
    print(f"  Données (max 5):")
    for row in rows:
        print(f"    {row}")

conn.close()