

from account_manager import AccountManager
from UserPermissions import UserPermissions


class AccountManagerSqlite(AccountManager):
   def __init__(self, dbpath):
      super(AccountManagerSqlite, self).__init__(dbpath)
      self.p = UserPermissions(dbpath)

   def user_get_id_from_name(self, uname=None, email=None):
      return self.p._get_uid(uname, email)

   def user_exists(self, uname, email=None):
      return self.p._user_exists(self, uname)
