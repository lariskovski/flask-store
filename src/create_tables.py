import sqlite3

# Create connection
conn = sqlite3.connect('data.db')
cursor = conn.cursor()

#########
# CREATE TABLE
#########
create_table = "CREATE TABLE IF NOT EXISTS users (id INTEGER PRIMARY KEY, username text, password text)"
cursor.execute(create_table)

create_table = "CREATE TABLE IF NOT EXISTS items (name text, price real)"
cursor.execute(create_table)


# Commit and close connection
conn.commit()
conn.close()
