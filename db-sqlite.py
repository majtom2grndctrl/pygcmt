import sqlite3, datetime, time
from pytz import timezone

var_now = datetime.datetime.now(timezone('UTC'))

conn = sqlite3.connect('gcmt.db')
conn.execute("CREATE TABLE user (id INTEGER PRIMARY KEY, firstName char(255) NOT NULL, lastName char(255) NOT NULL, bio TEXT)")
conn.execute("CREATE TABLE blogpost (id INTEGER PRIMARY KEY, title char(255) NOT NULL, status char(15), author INTEGER NOT NULL, published INT, slug TEXT, content TEXT, excerpt TEXT, FOREIGN KEY(author) REFERENCES user(id) ON DELETE CASCADE)")
conn.execute("INSERT INTO user VALUES (NULL, 'Dan', 'Hiester', 'This author has blogged for over a decade, and has recently started developing their own blog publishing platform.')")
conn.execute("INSERT INTO blogpost VALUES (?, ?, ?, ?, ?, ?, ?, ?)", (None, 'Hello World', 'Published', 1, var_now.strftime('%s'), None, 'This is just a test entry. Please delete it when you sign in to the backend.', 'This is just a test entry. Please delete it when you sign in to the backend.'))
time.sleep(10)
var_now = datetime.datetime.now(timezone('UTC'))
conn.execute("INSERT INTO blogpost VALUES (?, ?, ?, ?, ?, ?, ?, ?)", (None, 'Hello Again', 'Published', 1, var_now.strftime('%s'), None, 'This is the second test entry. Please delete it when you sign in to the backend.', 'This is the second test entry. Please delete it when you sign in to the backend.'))

conn.commit()

