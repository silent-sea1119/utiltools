import sqlite3, json
import uuid

class Db:
   '''Database Helper Class'''

   def __init__(self, path, table_name): #path = 'test.db'
      '''

      Args:
         path: path to sqlite file
         table_name: name for this table
      '''

      self.conn = sqlite3.connect(path)
      self.table_name = table_name

      self.setup() #derived class function

   def init_db_setup(self, columns):
      cmd = 'CREATE TABLE if not exists %s (' % (self.table_name, )

      for i, col in enumerate(columns):
         cmd += col[0] + ' ' + col[1]
         if len(col) == 3:
            cmd += ' '  + col[2]
         if len(col) == 4:
            cmd += ' ' + col[2] + ' ' + col[3]

         if i+1 < len(columns):
            cmd += ', '

      cmd += ')'

      print(cmd)
      self.exec_cmd(cmd)

   def get_len(self):
      cmd = 'SELECT Count(*) FROM %s' % (self.table_name,)
      ret = self.exec_cmd(cmd, is_fetch=True)
      return ret

   def shutdown(self):
      #self.c.close()
      pass

   def exec_cmd(self, cmd, args=None,
                is_fetch=False, is_fetch_mult=False,
                mult_fetch_max_args=None):
      self.c = self.conn.cursor()

      if args is not None:
         self.c.execute(cmd, args)
      else:
         self.c.execute(cmd)

      ret = None
      if is_fetch:
         ret = self.c.fetchone()
      elif is_fetch_mult:
         ret = []
         i = 0
         done = False

         while not done:
            entry = self.c.fetchone()
            i += 1
            if entry is None or i > mult_fetch_max_args:
               done = True
            else:
               ret.append(entry)

         return ret
      else:
         self.conn.commit()
      self.c.close()

      return ret


   def search(self, search_col, search_val, search_max=100):
      args = (self.table_name, search_col)
      cmd = "SELECT * FROM %s WHERE %s LIKE ?" % args
      va_args = {
         'is_fetch_mult' : True,
         'mult_fetch_max_args' : search_max
      }
      ret_val = self.exec_cmd(cmd, [search_val], **va_args)
      return ret_val
      pass

   #def get_single_by_column(self, col_name, col_val):
   #   cmd = "SELECT * FROM %s WHERE %s = ?" % (self.table_name, col_name)

   def insert_list(self, lst):
      #self.c.executemany('INSERT INTO %s VALUES ('
      pass

   def insert(self, vals):
      cmd = 'INSERT INTO %s VALUES (' % (self.table_name,)

      for i, x in enumerate(vals):
         cmd += '?'
         if i < len(vals)-1:
            cmd += ', '

      cmd += ')'

      print(cmd)
      self.exec_cmd(cmd, args=tuple(vals))


########################

#Example

class PostDb(Db):
   def __init__(self, path):
      super().__init__(path, 'posts')

   def setup(self):
      columns = [
         ['id', 'integer', 'PRIMARY KEY', 'AUTOINCREMENT'],
         ['data', 'text'],
         ['title', 'text'],
      ]

      self.init_db_setup(columns)

   def get_by_id(self, post_id):
      cmd = "SELECT * FROM %s WHERE id = ?" % (self.table_name,)
      print(cmd)
      ret = self.exec_cmd(cmd, args=[int(post_id)], is_fetch=True)
      print(ret)
      return ret




