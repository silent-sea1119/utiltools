import os.path, sqlite3

class DbDict:
   def __init__(self, db_path):
      self.db_path = db_path

      need_init = False
      if not os.path.exists(db_path):
         need_init = True

      self.conn = sqlite3.connect(db_path)
      self.c = self.conn.cursor()

      if need_init:
         self.init_db()

   def init_db(self):
      #create_str = 'CREATE VIRTUAL TABLE %s USING fts4'
      create_str = 'CREATE TABLE %s'

      #init_code = '''%s (key string, val string)''' % (create_str % 'str_str')
      init_code = '''%s (key text primary key, val string)''' % (create_str % 'str_str')

      print(init_code)
      self.c.execute(init_code)
      #TODO: using whole string just to store integer? bad idea
      self.c.execute('''%s (key string, val integer)''' % (create_str % 'str_int'))
      self.c.execute('''%s (key integer, val string)''' % (create_str % 'int_str'))
      self.c.execute('''%s (key integer, val integer)''' % (create_str % 'int_int'))
      self.conn.commit()

   def set(self, key, val):
      #self.c.execute('INSERT INTO str_str VALUES (?, ?)', (key, val))
      self.c.execute('INSERT OR REPLACE INTO str_str (key, val) VALUES (?, ?)', (key, val))
      self.conn.commit()

   def get(self, key): #maybe pass defaultval
      self.c.execute('SELECT val FROM str_str WHERE key = ?', (key, ))
      ret = self.c.fetchone()[0]
      if ret is None:
         return ret
      else:
         return ret[0]

