import sqlite3
#import pandas as pd

conn = sqlite3.connect(r'vivino.db')

cur = conn.cursor()

cur.execute("""
SELECT COUNT(DISTINCT group_name) FROM keywords_wine;
""")

print(cur.fetchall())
