#from events import Event
import os.path, sqlite3
from .atomicid import ObjId
from .dbdict import DbDict
#from secpass import PasswordDb
from .secpassdb import PasswordDb

def log(msg):
   print(msg)

class Db(object):
   '''Old Helper database class'''

   #dictionary of table names and their initialization code
   tables_need_exist = dict() #{ 'obj_ids', _init_obj_ids }

   def __init__(self, dbpath):
      self.dbpath = dbpath

      #self.need_init_all = False
      #if not os.path.exists(dbpath):
      #   self.need_init_all = True
      #   log('need to initialize all tables')

      self.conn = sqlite3.connect(dbpath, check_same_thread=False)
      self.c = self.conn.cursor()

      accounts_exist = self.check_if_table_exists('userdata')
      #self.accounts = PasswordDb(self.dbpath, not accounts_exist, self.get_obj_id)
      self.accounts = PasswordDb(self.conn, not accounts_exist, self.get_obj_id)

      #self.objids = ObjId(self.dbpath, not self.check_if_table_exists('obj_ids'))
      self.objids = ObjId(self.conn, not self.check_if_table_exists('obj_ids'))

      self.tables_need_exist['str_str'] = self._init_db_dict
      #self.tables_need_exist['userdata'] = self._init_userdata
      #self.tables_need_exist['obj_ids'] = self._init_obj_ids
      self.init_tables()

   def check_if_table_exists(self, tableName):
      self.c.execute('''SELECT name FROM sqlite_master
                        WHERE type='table' AND name=?''', (tableName,))
      ret = self.c.fetchone()
      if ret is None:
         return False
      else:
         return True

   #classes that inerit need to initialize
   #tables_need_exist first and the call this
   def init_tables(self):
      for name in self.tables_need_exist:
         need_init = False
         #if self.need_init_all:
         #   need_init = True
         #elif not self.check_if_table_exists(name):
         if not self.check_if_table_exists(name):
            need_init = True
         if need_init:
            log('creating and initing table %s' % name)
            init_func = self.tables_need_exist[name]
            init_func()

   #def _init_obj_ids(self):
   #   self.objids = ObjId(self.dbpath)
   #   self.objids.init_db()
   def _init_db_dict(self):
      self.dbdict = DbDict(self.dbpath)
      self.dbdict.init_db()
   def _init_userdata(self):
      self.accounts = PasswordDb(self.dbpath, True, self.get_obj_id)

   ###
   def get_obj_id(self, need_lock=True):
      return self.objids.get_id(need_lock)

   def dset(self, key, val):
      self.dbdict.set(key, val)
   def dget(self, key, val):
      return self.dbdict.get(key)

   def account_exists(self, uname):
      return self.accounts.check_if_user_exists(uname)

   #0 = success, 1 = username taken, 2 = bad username, 3 = bad password
   def add_account(self, uname, passw):
      return self.accounts.db_add_user(uname, passw)
   #0 = good password, 1 = username doesn't exist
   #2 = username doesn't match (internal check)
   #3 = password doesn't match, 4 = other error
   def check_account_match(self, uname, passw):
      return self.accounts.db_check_user(uname, passw)

   #pass

