#!/usr/bin/env python
from multiprocessing import Lock
import sqlite3

#from . import secpass
from utiltools import secpass


#from pycloak.shellutils import file_exists
from os.path import exists as file_exists

lock = Lock()
#TODO: serialize username and password

class PasswordDb:
   '''PaswordDB: secure user credential storage database'''

   def __init__(self, dbpath_or_conn = 'passwords.db',
                create_new = False, get_next_id=None,
                min_uname=6, min_pass=8, min_email=10):
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
      self.min_email = min_email

      if create_new:
         self.init_empty_db()

   def init_empty_db(self):
      self.c.execute('''CREATE TABLE userdata
                        (objid number, username text, email text, pass_hash text)''')
      self.conn.commit()
      pass

   def check_if_user_exists(self, uname=None, email=None):
      """Checks if user exists

      Tests
      """
      if uname is not None:
         self.c.execute("SELECT username FROM userdata WHERE username = ?", (uname, ))
         if self.c.fetchone() != None:
            return True
      if email is not None:
         self.c.execute("SELECT username FROM userdata WHERE email = ?", (email, ))
         if self.c.fetchone() != None:
            return True

      return False

   def _get_user_hash(self, uid):
      '''Get password has from uid'''
      self.c.execute("SELECT pass_hash FROM userdata WHERE objid = ?" % (uid, ))
      return self.c.fetchone()

   def new_user(self, password, uname=None, email=None):
      '''Add new user

         :param password: new user password
         :type password: string

         :param uname: new username
         :type uname: string

         :param email: user's email
         :type email: string

         :return: status code
         :rtype: int

         .. note::
            Status codes:
               * 0 = success
               * 1 = bad password
               * 2 = bad username
               * 3 = bad email
               * 4 = no email and no uname
               * 5 = username taken
               * 6 = email taken
      '''

      ###CODE

      if self.min_pass is not None and len(password) < self.min_pass:
         return 1

      if uname is not None:
         if self.min_uname is not None and len(uname) < self.min_uname:
            return 2

      if email is not None:
         if self.min_email is not None and len(email) < self.min_email:
            return 3

      if uname is None and email is None:
         return 4

      #kkkkkkk might needs this
      #kkkkkkk lock.acquire()
      if uname is not None:
         does_exist = self.check_if_user_exists(uname=uname)
         if does_exist:
            #kkkk might need this #lock.release()
            return 5
      if email is not None:
         does_exist = self.check_if_user_exists(email=email)
         if does_exist:
            return 6

      nextId = self.get_next_id(need_lock=False)
      pass_hash = secpass.gen_pass_hash(password)

      #kkkkkkkkk lock.release() #kkkkkkkkk might need this

      args = (nextId, uname, email, pass_hash) #pass_hash.replace('"', '""'))
      cmd = 'INSERT INTO userdata VALUES (?, ?, ?, ?)'
      self.c.execute(cmd, args)
      self.conn.commit()
      #lock.release()
      return 0

      ###END CODE

      pass #end db_add_user

   def check_user_login(self, password_check, username_check=None, email_check=None):
      '''Check username/password combo

      :param username_check: username to check
      :type username_check: string

      :param email_check: email to check
      :type email_check: string


      :param password_check: password to check
      :type oassword_check: string

      :return: status code
      :rtype: int

      .. note::
         Statuses:
         * 0 = good password
         * 1 = username/email doesn't exist
         * 2 = username or email doesn't match database data (internal)
         * 3 = password doesn't match
         * 4 = other error (selecting user data failed)
         * 5 = other error (getuid failed)
         * 6 = both username_check and email_check is none
      '''

      if username_check is None and email_check is None:
         return 6

      user_exists = self.check_if_user_exists(username_check, email_check)
      if not user_exists:
         return 1

      uid = self.get_uid_from_uname_email(username_check, email_check)
      if uid is None:
         return 5

      self.c.execute("SELECT * FROM userdata WHERE objid = ?", (uid, ))
      user = self.c.fetchone()
      if user is None:
         return 4

      #(uname, phash, salt, prepend) = user
      (uid, uname, email, phash) = user

      if not (username_check == uname or email == email_check):
         return 2

      #checker = secpass.SecurePassword()
      #checker.set_pass_info(phash, salt, prepend)
      #checker.check_pass(password_check):
      if secpass.check_pass_match(password_check, phash):
         return 0

      return 3

   def get_uid_from_uname_email(self, uname=None, email=None):
      if uname is not None:
         self.c.execute('SELECT objid FROM userdata WHERE username = ?', (uname, ))
      elif email is not None:
         self.c.execute('SELECT objid FROM userdata WHERE email = ?', (email, ))
      else:
         return None
      uId = self.c.fetchone()
      if uId is None or ((type(uId) is tuple) and uId[0] is None):
         return None

      return uId[0]

   #def rm_user_by_uname_email(self, uname=None, email=None):
   #   pass

   def rm_user_by_id(self, uid):
      self.c.execute('DELETE FROM userdata WHERE objid = ?', (uid, ))
      pass


   #pass #end PasswordDb


###TESTS

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
   pass

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

   pass


###END TESTS

