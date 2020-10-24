import sqlite3

connection = sqlite3.connect('data.db')
cursor = connection.cursor()
# to select and start things
create_table = "CREATE TABLE users (id int,username text,password text)"
cursor.execute(create_table)

user = (1,'sai','asdf')
insert_query = "INSERT INTO users VALUES (?,?,?)"
cursor.execute(insert_query,user)

users = [
    (3,'sai7','asdf'),
    (4,'sai9','asdf')
]

cursor.executemany(insert_query,users)

select_query = "SELECT * FROM users"
for row in cursor.execute(select_query):
    print(row)

connection.commit()
connection.close()