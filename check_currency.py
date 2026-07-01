import sqlite3

conn = sqlite3.connect(
    "business_intelligence.db"
)

cursor = conn.cursor()

cursor.execute(
    """
    SELECT *
    FROM currency
    """
)

rows = cursor.fetchall()

for row in rows:
    print(row)

conn.close()