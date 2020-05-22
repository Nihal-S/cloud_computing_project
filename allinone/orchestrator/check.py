import sqlite3
conn = sqlite3.connect('Rideshare.db')
c = conn.cursor()
query = "SELECT * FROM users"
c.execute(query)
rows = c.fetchall()
print(rows)
conn.commit()
conn.close()