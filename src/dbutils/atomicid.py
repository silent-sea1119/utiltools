from multiprocessing import Lock
import time, sqlite3, os.path

lock = Lock()

class ObjId:
   '''[Deprecated] Used to make atomic id's for tables; use primary keys instead '''

   def __init__(self, dbpath_or_conn, need_init = False):
      if type(dbpath_or_conn) is str:
         if not os.path.exists(dbpath_or_conn):
            need_init = True

         self.conn = sqlite3.connect(dbpath_or_conn)
      else:
         self.conn = dbpath_or_conn

      self.c = self.conn.cursor()

      if need_init:
         self.init_db()

      #pass

   def init_db(self):
      lock.acquire()
      self.c.execute('''CREATE TABLE obj_ids (objindex integer)''')
      self.c.execute('''INSERT INTO obj_ids VALUES (0)''')
      self.conn.commit()
      lock.release()

   def get_id(self, need_lock=True):
      '''get next index'''
      if need_lock:
         lock.acquire()
      self.c.execute('''SELECT objindex FROM obj_ids''')
      ret = self.c.fetchone()[0]
      pair = (ret+1, ret)
      self.c.execute('''UPDATE obj_ids SET objindex=? where objindex=?''', pair)
      self.conn.commit()
      if need_lock:
         lock.release()
      return ret

   #pass


