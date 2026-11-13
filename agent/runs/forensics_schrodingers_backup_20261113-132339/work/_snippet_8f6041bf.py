import sqlite3

# Ouvrir la base de données
conn = sqlite3.connect('catalog.db')
cursor = conn.cursor()

# Lister les tables
cursor.execute("SELECT name FROM sqlite_master WHERE type='table'")
tables = cursor.fetchall()
print("Tables:", tables)

# Pour chaque table, afficher le schéma
for table in tables:
    table_name = table[0]
    print(f"\n--- Table: {table_name} ---")
    cursor.execute(f"PRAGMA table_info({table_name})")
    columns = cursor.fetchall()
    for col in columns:
        print(f"  {col}")
    
    # Afficher les données
    cursor.execute(f"SELECT * FROM {table_name}")
    rows = cursor.fetchall()
    print(f"  Données ({len(rows)} lignes):")
    for row in rows:
        print(f"    {row}")

conn.close()