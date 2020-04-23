import sqlite3
conn = sqlite3.connect('Rideshare.db')
c = conn.cursor()

c.execute('''CREATE TABLE users
             (username VARCHAR(50) PRIMARY KEY, password VARCHAR(50) NOT NULL)''')

c.execute('''CREATE TABLE Areaname
             (Area_no INTEGER(5) PRIMARY KEY, Area_name VARCHAR(50))''')

c.execute('''CREATE TABLE ride
            (ride_id INTEGER PRIMARY KEY AUTOINCREMENT,created_by VARCHAR(50) NOT NULL, timestamp VARCHAR(19) NOT NULL,source INTEGER NOT NULL,destination INTEGER NOT NULL, foreign key(created_by) references users(username) on delete cascade,foreign key(source) references Areaname(Area_no) on delete cascade,foreign key(destination) references Areaname(Area_no) on delete cascade)''')

c.execute('''CREATE TABLE join_ride(   
            ride_id INTEGER(5),username VARCHAR(50),foreign key(ride_id) references ride(ride_id) on delete cascade,foreign key(username) references users(username) on delete cascade)''')

# Save (commit) the changes
conn.commit()

# We can also close the connection if we are done with it.
# Just be sure any changes have been committed or they will be lost.
conn.close()
