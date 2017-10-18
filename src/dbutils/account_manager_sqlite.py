
try:
   from account_manager import AccountManager, ACCOUNT_MANAGER_ERROR_TYPES
   from UserPermissions import UserPermissions
   from secpassdb import PasswordDb
except Exception as e:
   from .account_manager import AccountManager, ACCOUNT_MANAGER_ERROR_TYPES
   from .UserPermissions import UserPermissions
   from .secpassdb import PasswordDb

from utiltools.maybe import Maybe
from utiltools.miscutils import enum_helper

AMET = ACCOUNT_MANAGER_ERROR_TYPES



def mk_err(str_code, source=None, j={}):
   '''
   source=None/'perms'/'creds'
   '''

   j['source'] = source
   return Maybe(j, err_code=enum_helper(AMET, str_code))

def mk_succ(ret):

   return Maybe(ret)

'''Uses UserPermissions for user checks/etc (secpassdb not used to track user list)'''

class AccountManagerSqlite(AccountManager):

   def __init__(self, dbpath):
      super(AccountManagerSqlite, self).__init__(dbpath)

      self.perms = UserPermissions(dbpath)

      #self.creds = PasswordDb(dbpath)
      self.creds = PasswordDb(self.perms.conn, get_next_id=self.perms.get_obj_id)
      pass


   '''user_{get_id_from_name}'''

   def user_get_id_from_name(self, uname=None, email=None):
      return self.perms._get_uid(uname, email)

   '''end user_{get_id_from_name}'''

   '''user_{exists,add,rm,check_login}'''

   def user_exists(self, uname=None, email=None):
      return self.perms.user_exists(uname, email)

   def user_add(self, passw, uname=None, email=None):
      '''Add new user'''

      uname_exists_perms = self.perms.user_exists(uname=uname)
      email_exists_perms = self.perms.user_exists(email=email)

      #user_exists_creds = self.creds.check_if_user_exists(uname, email)
      uname_exists_creds = self.creds.check_if_user_exists(uname=uname)
      email_exists_creds = self.creds.check_if_user_exists(email=email)

      if uname_exists_perms or uname_exists_creds:
         source = None
         if uname_exists_perms:
            source = 'perms'
         if uname_exists_creds:
            source = 'creds'
         return mk_err('USERNAME_ALREADY_EXISTS', source)

      if email_exists_perms or email_exists_creds:
         source = None
         if email_exists_perms:
            source = 'perms'
         if email_exists_creds:
            source = 'creds'
         return mk_err('EMAIL_ALREADY_EXISTS', source)

      if uname is None and email is None:
         return mk_err('MISSING_USERNAME_AND_EMAIL')

      new_user_perms_ret = self.perms.new_user(uname, email)
      if new_user_perms_ret == 2:
         return mk_err('USERNAME_TOO_SHORT', 'perms')
      if new_user_perms_ret == 3:
         return mk_err('EMAIL_TOO_SHORT', 'perms')
      if new_user_perms_ret == 3:
         return mk_err('EMAIL_TOO_SHORT', 'perms')
      if new_user_perms_ret == 6:
         return mk_err('MISSING_USERNAME_AND_EMAIL', 'perms')

      if not (new_user_perms_ret == 1):
         return mk_err('UNKNOWN', 'perms', {'perms_code':new_user_perms_ret})


      new_user_creds_ret = self.creds.new_user(passw, uname, email)
      if new_user_creds_ret == 1:
         return mk_err('PASSWORD_TOO_SHORT', 'creds')
      if new_user_creds_ret == 2:
         return mk_err('USERNAME_TOO_SHORT', 'creds')
      if new_user_creds_ret == 3:
         return mk_err('EMAIL_TOO_SHORT', 'creds')
      if new_user_creds_ret == 4:
         return mk_err('MISSING_USERNAME_AND_EMAIL', 'creds')


      if new_user_creds_ret == 0:
         return mk_succ('SUCCESS')

      #if not (new_user_creds_ret == 0):
      #   return mk_err('UNKNOWN', 'creds', {'creds_code':new_user_creds_ret})

      return mk_err('UNKNOWN', 'creds', {'ret':(new_user_creds_ret, new_user_perms_ret)})

      pass

   def idkwhat_this_is():
      #self.user_perms.
      #self.creds.
      #x
      pass

   def user_rm(self, uid):
      '''Remove user'''
      uname_email = self.perms._get_uname_email_from_uid(uid)

      #self.perms.rm_user(
      pass

   def user_check_login(self, passw, uname=None, email=None):
      '''Check if login credentials match'''

      ret = self.creds.check_user_login(passw, uname, email)

      if ret == 6:
         return mk_err('MISSING_USERNAME_AND_EMAIL', 'perms')

      if ret == 3:
         return mk_err('PASSWORD_MISMATCH', 'perms')

      if ret == 1:
         return mk_err('USERNAME_OR_EMAIL_DOESNT_EXIST', 'perms')

      if ret == 0:
         return mk_succ('SUCCESS')

      if (ret in [2,4,5]) or True: #always do this
         return mk_err('UNKNOWN', 'perms', {'perms_code':ret})

      return mk_err('UNKNOWN')

      pass

   '''end user_{exists,add,rm,check_login}'''


   #pass


