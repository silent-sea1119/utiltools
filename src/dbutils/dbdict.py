import os.path, sqlite3

class DbDict:
   '''Sqlite3 dictionary implementation'''

   def __init__(self, db_path):
      self.db_path = db_path

      need_init = False
      if not os.path.exists(db_path):
         need_init = True

      self.conn = sqlite3.connect(db_path)
      self.c = self.conn.cursor()

      if need_init:
         self.init_db()

      pass #end __init__

   def init_db(self):
      '''Internal function called from __init__ if table doesn't exist'''
      #create_str = 'CREATE VIRTUAL TABLE %s USING fts4'
      create_str = 'CREATE TABLE %s'

      #init_code = '''%s (key string, val string)''' % (create_str % 'str_str')
      init_code = '''%s (key text primary key, val string)''' % (create_str % 'str_str')

      print(init_code)
      self.c.execute(init_code)
      #TODO: using whole string just to store integer? bad idea
      self.c.execute('''%s (key string PRIMARY KEY, val integer)''' % (create_str % 'str_int'))
      self.c.execute('''%s (key integer PRIMARY KEY, val string)''' % (create_str % 'int_str'))
      self.c.execute('''%s (key integer PRIMARY KEY, val integer)''' % (create_str % 'int_int'))
      self.conn.commit()

   def set(self, key, val, table_name='str_str'):
      '''Set key value'''
      #self.c.execute('INSERT INTO str_str VALUES (?, ?)', (key, val))
      self.c.execute('INSERT OR REPLACE INTO %s (key, val) VALUES (?, ?)' % (table_name,), (key, val))
      self.conn.commit()

   def get(self, key, table_name='str_str'): #maybe pass defaultval
      '''Get key value'''
      self.c.execute('SELECT val FROM %s WHERE key = ?' % (table_name,), (key, ))
      ret = self.c.fetchone()[0]
      if ret is None:
         return ret
      else:
         return ret[0]
      pass

   #pass end DbDict


