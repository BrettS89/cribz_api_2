import sqlite3

connection = sqlite3.connect('data.db')

cursor = connection.cursor()

create_table = 'CREATE TABLE IF NOT EXISTS users (id INTEGER PRIMARY KEY, email text, password text)'
cursor.execute(create_table)

create_table2 = 'CREATE TABLE IF NOT EXISTS cribs (id INTEGER PRIMARY KEY, url text, name text, price REAL, pictures TEXT, user INTEGER, created_date REAL, FOREIGN KEY(user) REFERENCES users(id))'
cursor.execute(create_table2)

connection.commit()

connection.close()