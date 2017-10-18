

ACCOUNT_MANAGER_ERROR_TYPES = [
   '',

   ##making new account
   'USERNAME_TOO_SHORT',
   'EMAIL_TOO_SHORT',
   'PASSWORD_TOO_SHORT', #perms only
   'USERNAME_ALREADY_EXISTS',
   'EMAIL_ALREADY_EXISTS',
   #end making new account

   #log-in in (perms only)
   'USERNAME_DOESNT_EXIST', #unused
   'EMAIL_DOESNT_EXIST', #unused
   'USERNAME_OR_EMAIL_DOESNT_EXIST', #log-in check
   'PASSWORD_MISMATCH',
   #end log-in check

   ##generic
   'MISSING_USERNAME_AND_EMAIL', #need at least 1 to register/log-in
   'UNKNOWN',
   'SUCCESS'
]


def abstract():
   raise NotImplementedError("Abstract class, child must over-write")

#clean abstract class for account management
class AccountManager:

   def __init__(self, dbpath):
      self.dbpath = dbpath


   #USER STUFF

   '''user_get_{id_from_name_email,name_email_from_id}'''
   def user_get_id_from_name_email(self, uname=None, email=None):
      abstract()  #pass
   def user_get_name_email_from_id(self, uid):
      '''Get user name and email from user id'''
      abstract()
      pass

   '''user_{exists,add,rm,check_login/change_uname/change_email/change_pass}'''
   def user_exists(self, uname=None, email=None):
      '''Check if user exists'''
      #abstract()
      pass
   def user_add(self, passw, uname=None, email=None):
      '''Add new user'''
      abstract()
      pass
   def user_rm(self, uid):
      '''Remove user'''
      abstract()
      pass
   def user_check_login(self, passw, uname=None, email=None):
      '''Check if login credentials match'''
      abstract()
      pass
   def user_change_uname(self, uid, new_name):
      '''Change username'''
      abstract()
      pass
   def user_change_email(self, uid, new_email):
      '''Change email'''
      abstract()
      pass
   def user_change_pass(self, uid, new_pass):
      '''Change user passwd'''
      abstract()
      pass

   #END USER STUFF


   #GROUP STUFF

   '''group_get_{id_from_name, name_from_id}'''
   def group_get_id_from_name(self, gname):
      '''Get group id from group name'''
      abstract()
      pass
   def group_get_name_from_id(self, gid):
      '''Get group name from group id'''
      abstract()
      pass

   '''group_{exists,add,rm,rename,get_list}'''
   def group_exists(self, gname):
      '''Check if group name exists'''
      abstract()
   def group_add(self, gname):
      '''Add new group'''
      abstract()
   def group_rm(self, gid):
      '''Remove group'''
      abstract()
      pass
   def group_rename(self, gid, new_name):
      '''Change group name'''
      abstract()
      pass

   def group_get_list(self):
      '''Get a list of all group id's'''
      abstract()
      pass

   '''group_{add_user/rm_user/get_member_users}'''
   def group_add_user(self, uid, gid):
      '''Add user to group'''
      abstract()
      pass
   def group_rm_user(self, uid, gid):
      '''Remove user from group'''
      abstract()
      pass
   def group_get_member_users(self, gid):
      '''Get members of a group'''
      abstract()
      pass

   def user_get_groups(self, uid):
      '''Get a list of groups a user is member off'''
      abstract()
      pass

   #END GROUP STUFF


   #RESOURCE STUFF

   '''resource_get_{id_from_name,name_from_id}'''
   def resource_get_id_from_name(rname):
      '''Get resource id from name'''
      abstract()
      pass
   def resource_get_name_from_id(rid):
      '''Get resource name from id'''
      abstract()
      pass

   '''resource_{exists/add/rm/rename}'''
   def resource_exists(self, rname):
      '''Check if resource exists'''
      abstract()
      pass
   def resource_add(eslf, rname):
      '''Add resource by name'''
      abstract()
      pass
   def resource_rm(self, rid):
      '''Remove resource by id'''
      abstract()
      pass
   def resource_rename(self, rid, newname):
      '''Rename resource'''
      abstract()
      pass

   '''resource_{add/get}_group_perms'''
   def resource_add_group_perms(self, rid, gid, perms, remove_old):
      '''Set group permissions for resource'''
      abstract()
      pass
   def resource_get_group_perms(self, rid, gid):
      '''Get resource permissions for a group'''
      abstract()
      pass

   '''resource_{get_user_perm,get_groups}'''
   def resource_get_user_perm(self, rid, uid):
      '''Get resource permissions for user'''
      abstract()
      pass
   def resource_get_groups(self, rid):
      '''Get a list of groups a resource is member off'''
      abstract()
      pass


   #decorator. Passes arg "allowed"
   def resource_name(name):
      pass

   #TODO:# !!!
   def resource(func): #decrator
      def func_wrapper(resource):
         if allowed():
            return func(resource)
         else:
            print('error')
            return perm_denied()

      return func_wrapper

   #END RESOURCE STUFF


   #pass #end AccountManager



