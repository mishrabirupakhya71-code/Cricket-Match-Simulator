import sqlite3
import sys

path = r"D:\New_project\cricket_data.db"
conn = sqlite3.connect(path)
cur = conn.cursor()
rows = cur.execute("SELECT name FROM sqlite_master WHERE type='table' ORDER BY name").fetchall()
print("TABLES")
for row in rows:
    print(row[0])
conn.close()
