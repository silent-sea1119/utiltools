
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

class AlchemyConfig:
   '''Main wrapper class for SQLAlchemy'''

   def __init__(self, eng = None, session = None, Session = None, debug = False):
      self.eng = eng
      self.session = session
      self.Session = Session
      self.debug = debug

      self.pool_recycle = None
      self.engine_path = None

      self._first_maria_timeout = True

      pass #end __init__

   def mariadb_reset(self):
      self.eng.dispose()
      #self.conn.close()
      new_self = AlchemyConfig.from_engine_path(self.engine_path, self.debug, self.pool_recycle)
      self.eng = new_self.eng
      self.session = new_self.session
      self.Session = new_self.Session

   def maria_timeout(self):
      import signal
      if not self._first_maria_timeout:
         self.mariadb_reset()

      self._first_maria_timeout = False

      def onTimeout(signum, frame):
         print('resetting AlchemyConfig engine (signal %s %s)' % (signum, frame))
         #self.mariadb_reset()
         self.maria_timeout()

      signal.signal(signal.SIGALRM, onTimeout)
      signal.alarm(self.pool_recycle)




   def from_engine_path(engine_path, debug=False, pool_recycle=None):
      '''Generate AlchemyConfig from path to engine'''

      if pool_recycle is None:
         #pool_recycle = 3600
         pool_recycle = 30 #90 #30 #so recently submitted surveys sync
      if pool_recycle == -1:
         pool_recycle = None

      eng = create_engine(engine_path, echo=debug, pool_recycle=pool_recycle)
      Session = sessionmaker(bind=eng)
      session = Session()

      ret = AlchemyConfig(eng, session, Session, debug=debug)
      ret.pool_recycle = pool_recycle
      ret.engine_path = engine_path

      if pool_recycle is not None:
         ret.maria_timeout()

      return ret


   def from_sqlite_file(db_path = None, debug=False, pool_recycle=None):

      driver = 'sqlite:'
      #driver = 'sqlite+pysqlite:'

      engine_path = driver + '//'
      if db_path is not None:
         engine_path = driver + '///' + db_path

      return AlchemyConfig.from_engine_path(engine_path, debug=debug)


   def from_eng_sesh(eng, sesh, debug=False):
      '''Generate AlchemyConfig from engine and session
      Keyword arguments:
      debug - do we pass debug to Alchemy Constructor'''

      return AlchemyConfig(eng, sesh, debug=debug)


   def from_creds(uname, passw, db_name, db_backend='mysql', debug = False):
      engine_path_args = (db_backend, uname, passw, db_name)
      engine_path = '%s://%s:%s@localhost/%s' % engine_path_args
      return AlchemyConfig.from_engine_path(engine_path, debug=debug)

   #first line uname, second line password
   def from_creds_file_path(creds_path, db_name, debug = False, db_backend='mysql'):
      user, passw = AlchemyConfig.get_mariadb_creds(creds_path)
      return AlchemyConfig.from_creds(user, passw, db_name, db_backend=db_backend, debug = debug)

   def get_mariadb_creds(creds_path):
      user = None
      passw = None
      with open(creds_path) as f:
         cred_lines = f.read().split('\n')
         user = cred_lines[0]
         passw = cred_lines[1]
      return user, passw

   #pass




