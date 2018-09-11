import sqlite3

class userdb:
    def __init__(self, db):
        self.db = db
        conn = sqlite3.connect(self.db)
        c = conn.cursor()
        c.execute('CREATE TABLE IF NOT EXISTS users (username text, password text)')
        if not self.find('admin'):
            c.execute("INSERT INTO users VALUES ('admin', 'admin')")
            conn.commit()

    def find(self, username):
        conn = sqlite3.connect(self.db)
        c = conn.cursor()
        res = c.execute('SELECT COUNT(*) FROM users WHERE username = ?', (username, ))
        return bool(res.fetchone()[0])

    def login(self, username, password):
        conn = sqlite3.connect(self.db)
        c = conn.cursor()
        res = c.execute('SELECT COUNT(*) FROM users WHERE username = ? and password = ?', (username, password))
        return bool(res.fetchone()[0])

    def register(self, username, password):
        conn = sqlite3.connect(self.db)
        c = conn.cursor()
        if not self.find('username'):
            c.execute('INSERT INTO users VALUES (?, ?)', (username, password))
            conn.commit()
            return True
        else:
            return False
