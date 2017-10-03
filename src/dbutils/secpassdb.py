#!/usr/bin/env python
from multiprocessing import Lock
import sqlite3
from . import secpass
#from pycloak.shellutils import file_exists
from os.path import exists as file_exists
#from . import secpass

lock = Lock()
#TODO: serialize username and password

class PasswordDb:
   '''PaswordDB'''

   def __init__(self, dbpath_or_conn = 'passwords.db',
                create_new = False, get_next_id=None,
                min_uname=6, min_pass=8):
      """Init function

      Args:
         dbpath_or_conn: database path
      """
      if type(dbpath_or_conn) is str:
         if not file_exists(dbpath_or_conn):
            create_new = True
         self.conn = sqlite3.connect(dbpath_or_conn, check_same_thread=False)
      else:
         self.conn = dbpath_or_conn

      self.c = self.conn.cursor()
      if get_next_id is None:
         get_next_id = lambda: 0
      self.get_next_id = get_next_id

      self.min_uname = min_uname #if None, then don't check
      self.min_pass = min_pass #if passed None, then don't check

      if create_new:
         self.init_empty_db()

   def init_empty_db(self):
      self.c.execute('''CREATE TABLE userdata
                        (objid number, username text, pass_hash text)''')
      self.conn.commit()

   def check_if_user_exists(self, uname):
      """Checks if user exists

      Tests
      """
      self.c.execute("SELECT username FROM userdata WHERE username = ?", (uname, ))
      if self.c.fetchone() != None:
         return True
      return False

   def get_user_hash(self, uname):
      self.c.execute("SELECT pass_hash FROM userdata WHERE username = ?" % (uname, ))
      return self.c.fetchone()

   #0 = success, 1 = username taken, 2 = bad username, 3 = bad password
   #TODO: this is outdated:::: , 4 = SecurePass error
   def db_add_user(self, username, password):
      if self.min_uname is not None and len(username) < self.min_uname:
         return 2
      if self.min_pass is not None and len(password) < self.min_pass:
         return 3

      #kkkkkkk might needs this
      #kkkkkkk lock.acquire()
      does_exist = self.check_if_user_exists(username)
      if does_exist:
         #kkkk might need this #lock.release()
         return 1

      nextId = self.get_next_id(need_lock=False)
      pass_hash = secpass.gen_pass_hash(password)
      #sp = secpass.SecurePassword()
      #new_user = sp.set_pass(password)
      #if new_user is None:
      #   return 4
      #(phash, salt, prepend) = new_user
      #kkkkkkkkk might need this
      #kkkkkkkkk lock.release()
      args = (nextId, username, pass_hash) #pass_hash.replace('"', '""'))
      cmd = 'INSERT INTO userdata VALUES (?, ?, ?)'
      self.c.execute(cmd, args)
      self.conn.commit()
      #lock.release()
      return 0

   #0 = good password, 1 = username doesn't exist
   #2 = username doesn't match (internal)
   #3 = password doesn't match, 4 = other error
   def db_check_user(self, username_check, password_check):
      user_exists = self.check_if_user_exists(username_check)
      if not user_exists:
         return 1

      self.c.execute("SELECT * FROM userdata WHERE username = ?", (username_check, ))
      user = self.c.fetchone()
      if user is None:
         return 4

      #(uname, phash, salt, prepend) = user
      (uid, uname, phash) = user

      if username_check != uname:
         return 2

      #checker = secpass.SecurePassword()
      #checker.set_pass_info(phash, salt, prepend)
      #checker.check_pass(password_check):
      if secpass.check_pass_match(password_check, phash):
         return 0
      return 3



#TESTS

def add_user(i):
   uname = 'user' + str(i)
   upass = 'pass' + str(i)
   x = PasswordDb()
   res = x.db_add_user(uname, upass)
   #print('adding %s %s: %i' % (uname, upass, res))

def check_user(i):
   uname = 'user' + str(i)
   upass = 'pass' + str(i)
   x = PasswordDb()

   res = x.db_check_user(uname, upass)
   #print('checking user: %s %s: %i' % (uname, upass, res))
   upass = 'pass' + str(i+1)
   res = x.db_check_user(uname, upass)
   #print('checking user: %s %s: %i' % (uname, upass, res))

def test_concurr():
   from multiprocessing import Pool
   p = Pool(5)
   p2 = Pool(5)

   user = 'user'
   passw = 'pass'

   p.map(add_user, range(2000, 2500))
   p2.map(check_user, range(200, 2500))
   #for i in range(2100, 2200):
      #p.map(add_user, range(i, i+5))
      #p2.map(check_user, range(i, i+5))
      #p.map(add_user, range(i, i+5))

#first run should print: 0 0 3 1, second run: 1 0 3 1
def test_db(pdb):
   res = pdb.db_add_user('testuser', 'password')
   print(res)
   res = pdb.db_check_user('testuser', 'password')
   print(res)
   res = pdb.db_check_user('testuser', 'p')
   print(res)
   res = pdb.db_check_user('baduser', 'password')
   print(res)

if __name__ == '__main__':
   #x = PasswordDb(create_new = True)
   loc = 'passwords.db'
   create_new = not file_exists(loc)
   pdb = PasswordDb(loc, create_new=create_new)

   #test_concurr()
   test_db(pdb)


