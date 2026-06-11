import sqlite3

conn = sqlite3.connect('../backend/test.db')
cursor = conn.cursor()
cursor.execute("SELECT id, status, role FROM users LIMIT 5")
for row in cursor.fetchall():
    print(row)
