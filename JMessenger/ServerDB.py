import sqlite3

class ServerDB(object):
    def __init__(self):
        self.con = sqlite3.connect(":memory:")
        self.cur = self.con.cursor()
        self.cur.execute("CREATE TABLE IF NOT EXISTS user(id text, pw text, ison int, primary key(id));")

    def joinuser(self,id,pw):
        try:
            self.cur.execute("INSERT INTO user VALUES(?,?,?);",(id,pw,0))
            return True
        except Exception as e:
            print(e.args)
            return False
