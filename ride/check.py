import sqlite3
conn = sqlite3.connect('Rides.db')
c = conn.cursor()

c.execute("select * from ride")

rows = c.fetchall()
print(rows)

conn.commit()
conn.close()