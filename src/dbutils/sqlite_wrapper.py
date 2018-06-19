import sqlite3, json
import uuid


class Db:
   '''Database Helper Class'''

   def __init__(self, path, table_name=None): #path = 'test.db'
      '''

      Args:
         path: path to sqlite file
         table_name: name for this table
      '''

      self.conn = sqlite3.connect(path)
      self.table_name = table_name

      self.setup() #derived class function

   def setup(self):
      '''Virtual function for creating tables/etc'''

      '''
      columns = [
         ['id', 'integer', 'PRIMARY KEY', 'AUTOINCREMENT'],
         ['timestamp', 'integer'],
         ['data', 'text'],
         ['email', 'VARCHAR(35)']
      ]
      self.init_db_setup(columns)
      '''

      raise NotImplementedError("Abstract class, child must over-write")

   def init_db_setup(self, columns):
      '''Creates table from columns'''
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

   def check_if_table_exists(self, tableName=None):
      self.c.execute('''SELECT name FROM sqlite_master
                        WHERE type='table' AND name=?''', (tableName,))
      ret = self.c.fetchone()
      if ret is None:
         return False
      else:
         return True

      pass #end check_if_table_exists

   def get_len(self):
      '''Get table row count'''
      cmd = 'SELECT Count(*) FROM %s' % (self.table_name,)
      ret = self.exec_cmd(cmd, is_fetch=True)
      return ret

   def shutdown(self):
      #self.c.close()
      pass

   #either is_fetch, is_fetch_mult or fast_fetch. if all false, executes query and doesn't fetch result
   def exec_cmd(self, cmd, args=None,
                is_fetch=False, is_fetch_mult=False,
                mult_fetch_max_args=None,
                fast_fetch=False):
      '''Execute database command

      '''
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
            #pass end loop

         return ret
      elif fast_fetch:
         ret = self.c.fetchall()
      else:
         self.conn.commit()
      self.c.close()

      return ret


   def get_single_by_column(self, col_name, col_val):
      args = (self.table_name, col_name)
      cmd = 'SELECT * FROM %s WHERE %s = ?' % args

      data = self.exec_cmd(cmd, (col_val,), is_fetch=True)
      return data

   #def get_single_by_column(self, col_name, col_val):
   #   cmd = "SELECT * FROM %s WHERE %s = ?" % (self.table_name, col_name)
   #pass

   def search(self, search_col, search_val, search_max=100):
      '''Search table'''

      args = (self.table_name, search_col)
      cmd = "SELECT * FROM %s WHERE %s LIKE ?" % args
      va_args = {
         'is_fetch_mult' : True,
         'mult_fetch_max_args' : search_max
      }
      ret_val = self.exec_cmd(cmd, [search_val], **va_args)

      return ret_val

   def get_page_by_column(self, search_clause=None, search_vals=None, num_per_row=10, start_row=0):
      '''search_clause:
            "column_name LIKE ?"
            "column_name = ?"
         search_arg:
            [column_val]
      '''

      cmd = 'SELECT * FROM %s ' % (self.table_name)

      if search_clause is not None:
         cmd += 'WHERE ' + search_clause

      cmd += 'LIMIT ? OFFSET ?'

      args = []
      if search_vals is not None:
         args = search_vals

      args += [num_per_row, start_row]

      data = self.exec_cmd(cmd, tuple(args), fast_fetch=True)

      return data

   def insert_list(self, rows):
      self.c = self.conn.cursor()

      cmd = 'INSERT INTO %s VALUES (' % (self.table_name,)
      row_len = len(rows[0])

      for i in range(0, row_len-1):
         cmd += '?, '
         #pass

      cmd += '?)'

      #print(cmd)

      self.c.executemany(cmd, rows)
      self.conn.commit()

      self.c.close()

      pass

   def insert(self, vals):
      '''Insert value into table'''

      cmd = 'INSERT INTO %s VALUES (' % (self.table_name,)

      for i, x in enumerate(vals):
         cmd += '?'
         if i < len(vals)-1:
            cmd += ', '

      cmd += ')'

      #print(cmd)
      self.exec_cmd(cmd, args=tuple(vals))

      pass #end insert

   pass #end Db


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

   #pass



