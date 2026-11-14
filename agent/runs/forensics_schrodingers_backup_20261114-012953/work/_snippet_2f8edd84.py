import sqlite3
conn = sqlite3.connect('catalog.db')
cursor = conn.cursor()
cursor.execute("SELECT name FROM sqlite_master WHERE type='table';")
tables = cursor.fetchall()
print("Tables:", tables)
for table in tables:
    t = table[0]
    cursor.execute(f"PRAGMA table_info({t});")
    cols = cursor.fetchall()
    print(f"\nTable {t}:")
    for col in cols:
        print(f"  {col}")
conn.close()