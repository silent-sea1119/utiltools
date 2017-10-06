

#clean abstract class for account management
class AccountManager:

   def __init__(self, dbpath):
      self.dbpath = dbpath

   '''user_{get_id_from_name,exists,add,rm,check_login}'''
   def user_get_id_from_name(self, uname=None, email=None):
      pass
   def user_exists(self, uname=None, email=None):
      '''Check if user exists'''
      pass
   def user_add(self, passw, uname=None, email=None):
      '''Add new user'''
      pass
   def user_rm(self, uid);
      '''Remove user'''
      pass
   def user_check_login(self, passw, uname=None, email=None):
      '''Check if login credentials match'''
      pass


   '''group_{get_id_from_name,exists,add,rm,get_list}'''
   def group_get_id_from_name(self, gname):
      '''Get group id from group name'''
      pass
   def group_exists(self, gname):
      '''Check if group name exists'''
      pass
   def group_add(self, gname):
      '''Add new group'''
      pass
   def group_rm(self, gid):
      '''Remove group'''
      pass
   def group_get_list(self):
      '''Get a list of all group id's'''
      pass

   '''group_{add_user/rm_user}'''
   def group_add_user(self, uid, gid):
      '''Add user to group'''
      pass
   def group_rm_user(self, uid, gid):
      '''Remove user from group'''
      pass

   def group_get_members(self, gid):
      '''Get members of a group'''
      pass

   def user_get_groups(self, uid):
      '''Get a list of groups a user is member off'''
      pass


   '''resource_{exists/add/rm/add_group_perms}'''
   def resource_exists(self, rname):
      '''Check if resource exists'''
      pass
   def resource_add(eslf, rname):
      '''Add resource by name'''
      pass
   def resource_rm(self, rid):
      '''Remove resource by id'''
      pass
   def resource_add_group_perms(self, rid, gid, perms, remove_old):
      '''Set group permissions for resource'''
      pass

   '''resource_{get_user_perm,get_group_perms,resource_get_groups}'''
   def resource_get_user_perm(self, rid, uid):
      '''Get resource permissions for user'''
      pass

   def resource_get_group_perms(self, rid, gid):
      '''Get resource permissions for a group'''
      pass

   def resource_get_groups(self, rid):
      '''Get a list of groups a resource is member off'''
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

   #pass end AccountManager



