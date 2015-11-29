import sqlite3

class ServerDB(object):
    def __init__(self):
        self.con = sqlite3.connect(":memory:")
        self.cur = self.con.cursor()
        self.cur.execute("CREATE TABLE IF NOT EXISTS user(id text, pw text, ison int, ip text, port int, primary key(id));")

    def joinuser(self,id,pw):
        try:
            self.cur.execute("INSERT INTO user VALUES(?,?,?,?,?);",(id,pw,0,'',0))
            return True
        except Exception as e:
            return False
    def loginuser(self,id,pw,add):
        try:
            self.cur.execute("SELECT pw FROM user WHERE id=?;",(id,))
            realpw = self.cur.fetchone()[0]
        except:
            return 'LOGINR FAIL NOSUCHID'
        if realpw != pw:
            return 'LOGINR FAIL WRONGPW'
        
        try:
            self.cur.execute("UPDATE user SET ison=1, ip=?,port=? WHERE id=?",(add[0],add[1],id))
            print("[LOGIN] ip : %s, port : %d, id : %s"%(add[0],add[1],id))
            return 'LOGINR SUCCESS'
        except:
            return 'LOGINR FAIL UNKNOWN'

    def conuser(self, id):
        try:
            self.cur.execute("SELECT ison, ip, port FROM user WHERE id=?;", (id,))
            other = self.cur.fetchone()
        except Exception as e:
            print(e.args)
            return 'CONR FAIL UNKNOWN'
        if other is None:
            return 'CONR FAIL NO_SUCH_USER'
        if other[0] == 0:
            return 'CONR FAIL USER_NOT_ONLINE'
        return other[1:]

    def logoutuser(self, id):
        try:
            self.cur.execute("SELECT ison FROM user WHERE id=?;",(id,))
            ison = self.cur.fetchone()[0]
        except Exception as e:
            print(e.args)
            return 'LOGOUTR FAIL'
        if ison == 0:
            return 'LOGOUTR FAIL'
        try:
            self.cur.execute("UPDATE user SET ison=0 WHERE id=?;",(id,))
        except Exception as e:
            print(e.args)
            return 'LOGOUTR FAIL'
        return 'LOGOUTR SUCCESS'