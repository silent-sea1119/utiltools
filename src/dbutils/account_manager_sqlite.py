

from account_manager import AccountManager
from UserPermissions import UserPermissions
from secpassdb import PasswordDb



class AccountManagerSqlite(AccountManager):
   def __init__(self, dbpath):
      super(AccountManagerSqlite, self).__init__(dbpath)


      self.user_perms = UserPermissions(dbpath)

      #self.creds = PasswordDb(dbpath)
      self.creds = PasswordDb(self.user_perms.conn)



   def user_get_id_from_name(self, uname=None, email=None):
      return self.p._get_uid(uname, email)

   def user_exists(self, uname=None, email=None):
      return self.p._user_exists(self, uname)

   def user_add(self, passw, uname=None, email=None):
      '''Add new user'''
      pass

   def user_rm(self, uid);
      '''Remove user'''
      pass

   def user_check_login(self, passw, uname=None, email=None):
      '''Check if login credentials match'''
      pass




