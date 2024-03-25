import sqlite3
#import pandas as pd

conn = sqlite3.connect(r'vivino.db')

cur = conn.cursor()

cur.execute("""
SELECT * FROM grapes;
""")

print(cur.fetchall())
