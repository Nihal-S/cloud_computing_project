import sqlite3
conn = sqlite3.connect('Users.db')
c = conn.cursor()

c.execute('''CREATE TABLE users
             (username VARCHAR(50) PRIMARY KEY, password VARCHAR(50))''')

conn.commit()
conn.close()