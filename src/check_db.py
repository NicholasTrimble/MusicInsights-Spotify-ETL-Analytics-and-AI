import sqlite3

conn = sqlite3.connect("data/warehouse.db")
cursor = conn.cursor()

cursor.execute("SELECT * FROM users")
print("Tables in the database:", cursor.fetchall())

cursor.execute("SELECT * FROM products")
print("\nSample data:")
for row in cursor.fetchall():
    print(row)

conn.close()