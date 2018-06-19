import sqlite3

#mk_db_select_opts(where='id = 5', order_by='pulse_index')
def mk_db_select_opts(where=None, order_by='rowid'):

   return {
      'where' : where,
      'order_by' : order_by,
   }

   pass

def gen_where_clause(opts):
   where = opts['where']

   where_clause='' if where is None else ' WHERE ' + where + ' '
   return where_clause

def gen_order_by_clause(opts):
   order_by = opts['order_by']
   order_clause = '' if order_by is None else ' ORDER BY ' + order_by + ' '
   return order_clause


class DbWrapper:

   def __init__(self, db_path):
      self.db_path = db_path
      self.conn = sqlite3.connect(db_path)

      pass

   def get_cursor(self):
      return self.conn.cursor()

   def select_table_row(self, table_name, row_num):
      c = self.get_cursor()
      cmd = "SELECT * FROM %s WHERE rowid=?" % (table_name, )
      c.execute(cmd, (row_num, ))
      ret = c.fetchone()
      c.close()
      return ret

   def select_all(self, table_name):
      c = self.get_cursor()
      cmd = "SELECT * FROM %s" % (table_name, )
      c.execute(cmd)
      ret = c.fetchall()
      c.close()
      return ret

   def select_table_range(self, table_name, start, end):
      c = self.get_cursor()
      cmd = 'SELECT * FROM %s WHERE rowid > ? and rowid < ?' % (table_name,)
      c.execute(cmd, (start, end))
      ret = c.fetchall()
      c.close()
      return ret


   def select_table_page(self, table_name, page_num, items_per_page=None, opts=None):
      c = self.get_cursor()

      if items_per_page is None:
         items_per_page = 1000

      if opts is None:
         opts = mk_db_select_opts(order_by='rowid')

      where_clause = gen_where_clause(opts)
      order_clause = gen_order_by_clause(opts)

      offset = page_num * items_per_page

      args = (table_name, where_clause, order_clause)
      cmd = 'SELECT * FROM %s %s %s LIMIT ? OFFSET ?' % args
      c.execute(cmd, (items_per_page, offset))
      ret = c.fetchall()
      c.close()
      return ret

   def select_by_field(self, table_name, field_name, field_val, is_single=True):
      c = self.get_cursor()
      cmd = "SELECT * FROM %s WHERE %s=?" % (table_name, field_name)
      c.execute(cmd, (field_val,))
      if is_single:
         ret = c.fetchone()
      else:
         ret = c.fetchall()
      c.close()
      return ret


   def check_table_exists(self, table_name):
      c = self.get_cursor()
      c.execute("SELECT count(*) FROM sqlite_master WHERE type='table' AND name=?", (table_name, ))
      ret = c.fetchone()[0]
      c.close()
      return ret == 1

   def get_table_col_names(self, table_name):
      c = self.get_cursor()

      cmd = "PRAGMA table_info(%s)" % (table_name,)
      c.execute(cmd)
      result = c.fetchall()
      c.close()

      ret = []
      for x in result:
         ret.append(x[1])

      return ret

   def get_db_table_names(self):
      '''Returns table in SQLite database'''
      c = self.get_cursor()
      c.execute("SELECT name FROM sqlite_master WHERE type='table'")
      col_names = c.fetchall()
      c.close()
      ret = []
      for col_tuple in col_names:
         ret.append(col_tuple[0])
      return ret

   pass


