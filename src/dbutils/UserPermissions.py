
import sqlite3, os.path, json
#from flask import Flask, request, send_from_directory
from . import dbhelpers, atomicid

#app = Flask(__name__)
#DB_PATH = '/tmp/permtest.db'


#users and groups need to be unique
class UserPermissions(dbhelpers.Db):
   '''User/Groups database'''

   #TODO: can make more generic, and each permission is a Tag
   def _init_perm_table(self):
      #TODO: remove this logic
      #if self.check_if_table_exists('perm_groups'):
      #   return

      self.c.execute('''CREATE TABLE perm_groups (objid integer, name text)''')
      self.c.execute('''CREATE TABLE perm_users (objid integer, name text)''')
      self.c.execute('CREATE TABLE perm_group_members (objid integer, group_id integer, user_id integer)')

      self.c.execute('''CREATE TABLE perm_resources (objid integer, name text)''')

      #group with id group_id has permissions to resource with id resource_id. Perm described in beginning
      self.c.execute('''CREATE TABLE perm_resource_allowed_groups
                                     (objid integer, resource_id integer, group_id integer, perms integer)''')
      self.conn.commit()

   def __init__(self, dbpath):
      #tname = 'perm'
      tname = 'perm_groups'
      self.tables_need_exist[tname] = self._init_perm_table
      super(UserPermissions, self).__init__(dbpath)
      #self.init_tables()

   def _get_gid(self, gname):
      self.c.execute('SELECT objid FROM perm_groups WHERE name = ?', (gname, ))
      gid = self.c.fetchone()
      if gid is None:
         return None
      return gid[0]

   def _get_uid(self, uname):
      self.c.execute('SELECT objid FROM perm_users WHERE name = ?', (uname, ))
      uid = self.c.fetchone()
      if uid is None or ((type(uid) is tuple) and uid[0] is None):
         return None
      return uid[0]

   #1 = success, 2 = failure already exists, 3 = failure bad name (short at least 4 chars)
   def new_user(self, uname):
      if len(uname) < 4:
         return 3
      if self._get_uid(uname) is not None:
         return 2
      self.c.execute('INSERT INTO perm_users VALUES (?, ?)', (self.get_obj_id(), uname))
      self.conn.commit()
      return 1

   def user_exists(self, uname):
      if self._get_uid(uname) is not None:
         return True
      return False

   #1 = sucess, 2 = user never existed, (possibly 3 = user is admin)
   def rm_user(self, uname):
      self.c.execute('SELECT objid FROM perm_users WHERE name = ?', (uname, ))
      uId = self.c.fetchone()

      uId = self._get_uid(uname)
      if uId is None:
         return 2
      self.c.execute('DELETE FROM perm_users WHERE objid = ?', (uId, ))
      self.conn.commit()
      return 1

   #1 = success, 2 = already exists
   def new_group(self, groupname):
      if self._get_gid(groupname) is not None:
         return 2
      self.c.execute('INSERT INTO perm_groups VALUES (?, ?)', (self.get_obj_id(), groupname))
      self.conn.commit()
      return 1

   #1 = success, 2 = failure doesn't exist
   def rm_group(groupname):
      groupId = self._get_gid(groupname)
      if groupId is None:
         return 2
      self.c.execute('DELETE FROM perm_groups WHERE objid = ?', (groupId, ))
      self.conn.commit()
      return 1

   #add_user_to_group(self, groupname, uname)
   #1 = success
   #2 = group doesn't exist
   #3 = user doesn't exist
   #4 = user already in group
   def add_user_to_group(self, groupname, uname):
      gId = self._get_gid(groupname)
      if gId is None:
         return 2

      uId = self._get_uid(uname)
      if uId is None:
         return 3

      self.c.execute('SELECT objid FROM perm_group_members WHERE group_id = ? AND user_id = ?', (gId, uId))
      objId = self.c.fetchone()
      if objId is not None:
         return 4

      self.c.execute('INSERT INTO perm_group_members VALUES (?, ?, ?)', (self.get_obj_id(), gId, uId))
      self.conn.commit()
      return 1

   #1 = success
   #2 = group doesn't exist
   #3 = user doesn't exist
   #4 = user not in group
   def rm_user_from_group(self, groupname, uname):
      gId = self._get_gid(groupname)
      if gId is None:
         return 2

      uId = self._get_uid(uname)
      if uId is None:
         return 3

      self.c.execute('SELECT objid FROM perm_group_members WHERE group_id = ? AND user_id = ?', (gId, uId))
      objId = self.c.fetchone()
      if objId is None:
         return 4
      objId = objId[0]

      self.c.execute('DELETE FROM perm_group_members WHERE objid = ?',  (objId, ))
      self.conn.commit()
      return 1

   #get_user_name_from_id(uid) => uname or None
   def get_user_name_from_id(self, uid):
      self.c.execute('SELECT name from perm_users WHERE objid = ?', (uid, ))
      ret = self.c.fetchone()
      if ret is None:
         return None
      return ret[0]

   #get_group_name_from_id(gid): returns None or gid
   def get_group_name_from_id(self, gid):
      self.c.execute('SELECT name from perm_groups WHERE objid = ?', (gid, ))
      ret = self.c.fetchone()
      if ret is None:
         return None
      return ret[0]

   #get_user_groups(uname)
   #wrong false: 1 = success
   #true: list = success
   #2 = user doesn't exist
   #3 = get_user_group_ids returned bad type
   #4 = couldn't get name of one of the group_id's
   def get_user_groups(self, uname):
      gIds = self.get_user_group_ids(uname)
      if type(gIds) is int:
         return gIds
      if type(gIds) is not list:
         return 3
      ret = []
      for gId in gIds:
         gName = self.get_group_name_from_id(gId)
         if gName is None:
            print('bad gId:' + str(gId))
            return 4
         ret.append(gName)
      return ret

   #get_user_group_ids()
   #list = success
   #(wrong) 1 = success
   #2 = user doesn't exist
   def get_user_group_ids(self, uname):
      uId = self._get_uid(uname)
      if uId is None:
         return 2
      self.c.execute('SELECT group_id from perm_group_members WHERE user_id = ?', (uId, ))
      ret = []
      while True:
         gid = self.c.fetchone()
         if gid is None:
            return ret
         ret.append(gid[0])
      return ret

   def _get_rid(self, res_name):
      self.c.execute('SELECT objid FROM perm_resources WHERE name = ?', (res_name, ))
      rid = self.c.fetchone()
      if rid is None:
         return None
      return rid[0]

   def _get_permid_by_ids(self, res_id, group_id):
      self.c.execute('''SELECT objid FROM perm_resource_allowed_groups WHERE
                           group_id = ? AND resource_id = ?''', (group_id, res_id))
      pid = self.c.fetchone()
      if pid is None or (type(pid) is tuple and pid[0] is None):
         return None
      return pid[0]

   def _get_permid_by_names(self, res_name, group_name):
      self.c.execute('''SELECT objid FROM perm_resource_allowed_groups WHERE
                           group_id = ? AND user_id = ?''', (gid, uid))
      return

   #new_resource(res_name)
   #1 = success
   #2 = resource already exists
   #3 = one of groups doesn't exist
   #declare resource, and its access rights
   def new_resource(self, res_name): #, groups=[]):
      rid = self._get_rid(res_name)
      if rid is not None:
         return 2
      rid = self.get_obj_id()
      self.c.execute('INSERT INTO perm_resources VALUES (?, ?)', (rid, res_name))
      self.conn.commit()

      #for group in groups:
      #   ret = self.perm_resource_add_group(group)
      #   if ret != 1:
      #      return ret
      return 1

   #resource_group_add_perms(self, res_name, group_name, perms, remove_old)
   #1 = success
   #2 = res_name resource doesn't exist, 3 = group_name doesn't exist
   #4 = (4, 'bad_perm', perm_init_status) #whenever perms passed are invalid
   #5 = record for this group/resource combo should exist, but can't find it
   def resource_group_add_perms(self, res_name, group_name, perms, remove_old=False):
      #rid = self._get_rid(rid,) #kkyy
      rid = self._get_rid(res_name)
      if rid is None:
         return 2
      gid = self._get_gid(group_name)
      if gid is None:
         return 3

      real_perm = Perm(perms)
      if real_perm.get_status() != 0:
         return (4, 'bad_perm', real_perm.get_status())

      pid_old_entry = self._get_permid_by_ids(rid, gid)
      if pid_old_entry is None:
         pid = self.get_obj_id() #permission id
         arg_tuple = (pid, rid, gid, real_perm.val)
         self.c.execute('INSERT INTO perm_resource_allowed_groups VALUES (?, ?, ?, ?)', arg_tuple)
      else:
         if not remove_old:
            self.c.execute('SELECT perms FROM perm_resource_allowed_groups WHERE objid = ?',
                                   (pid_old_entry, ))
            perms = self.c.fetchone()
            if perms is None or ((type(perms) is tuple) and  perms[0] is None):
               return 5
            old_perms = Perm(int(perms[0]))
            real_perm = Perm(real_perm.val | old_perms.val)

         self.c.execute('DELETE FROM perm_resource_allowed_groups WHERE objid = ?',
                        (pid_old_entry, ))

         arg_tuple = (pid_old_entry, rid, gid, real_perm.val)
         self.c.execute('INSERT INTO perm_resource_allowed_groups VALUES (?, ?, ?, ?)', arg_tuple)
      self.conn.commit()
      return 1

   #self.c.execute('SELECT perms FROM perm_resource_allowed_groups WHERE')
   def resource_group_rm_perms(self, perm_id, perms): #(res_name, group_name):
      pass

   def resource_group_drop_all_perms(self, perm_id): #resource_group_rm_all_perms()
      pass

   #get_resource_group_perms(self, res_name, group_name)
   #(1, Perm) = success, 2 = res_name doesn't exist, 3 = group_name doesn't exist
   #4 = (4, 'bad_perm', perm_init_status)
   #5 = record for this group/res combo should exist but can't find it
   def get_resource_group_perms(self, res_name, group_name):
      rid = self._get_rid(res_name)
      if rid is None:
         return 2
      gid = self._get_gid(group_name)
      if gid is None:
         return 3

      pid = self._get_permid_by_ids(rid, gid)
      if pid is None:
         return Perm(0)
      else:
         self.c.execute('SELECT perms FROM perm_resource_allowed_groups WHERE objid = ?',
                        (pid, ))
         perms = self.c.fetchone()
         if perms is None or ((type(perms) is tuple) and  perms[0] is None):
            return 5
         perms = Perm(int(perms[0]))
         if perms.get_status() != 0:
            return (4, 'bad_perm', perms.get_status())
         return perms
      pass #end get_resource_group_perms

   #get_resource_user_perms(resname, uname) => Perm()
   #1 = (1, perm) = good perm
   #2 = res_name doesn't exist
   #3 = user doesn't exist
   #4 = (4, user_name, ret_status) = get_user_groups() failed
   #5 = (5, group_name, res_name, ret_status) = get_resource_group_perms failed
   #6 = (6, Perm().get_status()) = failed constructing one perm from all group perms put together
   def get_resource_user_perms(self, res_name, uname):
      rid = self._get_rid(res_name)
      if rid is None:
         return 2
      uid = self._get_uid(uname)
      if uid is None:
         return 3

      groups = self.get_user_groups(uname)
      if type(groups) is not list:
         return (4, uname, groups)

      all_perms_num = 0
      for group_name in groups:
         perms_ret = self.get_resource_group_perms(res_name, group_name)
         #if type(perms_ret) is not list:
         #   return (5, group_name, res_name, perms_ret)
         #for perm in perms_ret:
         #   all_perms_num |= perm.val
         if type(perms_ret) is not Perm:
            return (5, group_name, res_name, perms_ret)
         all_perms_num |= perms_ret.val

      all_perms = Perm(all_perms_num)
      perm_status = all_perms.get_status()
      if perm_status != 0:
         return (6, perm_status)
      return (1, all_perms)

   #TODO
   #def modify_resource_rights(res_name):
   #   pass

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

   #get_user_list() => [str]
   def get_user_list(self):
      self.c.execute('SELECT name FROM perm_users')
      ret = []
      while True:
         uname = self.c.fetchone()
         if uname is None:
            break
         ret.append(uname[0])
      return ret

   def fetch_list(self):
      ret = []
      while True:
         x = self.c.fetchone()
         if x is None:
            break
         ret.append(x[0])
      return ret

   #get_group_members(self, group_name)
   #[] = list success
   #1  = bad gname
   ###############false bad info ######2  = (2, bad_user_id)
   def get_group_members(self, group_name):
      gid = self._get_gid(group_name)
      if gid is None:
         return 1
      self.c.execute('SELECT user_id FROM perm_group_members WHERE group_id = ?', (gid, ))
      users_id_lst = self.fetch_list()
      ret = []
      for user_id in users_id_lst:
         uname = self.get_user_name_from_id(user_id)
         if uname is None:
            break
         ret.append(uname)
      return ret

   def get_group_list(self): # => [str]
      self.c.execute('SELECT name FROM perm_groups')
      ret = []
      while True:
         uname = self.c.fetchone()
         if uname is None:
            break
         ret.append(uname[0])
      return ret

   #pass #end class


'''
n = 0

class FormDb:
   def __init__(self):
      need_init = False
      if not os.path.exists(DB_PATH):
         need_init = True

      self.conn = sqlite3.connect(DB_PATH)
      self.c = self.conn.cursor()

      if need_init:
         self.init_db()

   def init_db(self):
      self.c.execute('CREATE TABLE contact_form (first_name text)')
      self.conn.commit()

   def add_contact(self, first):
      self.c.execute('INSERT INTO contact_form VALUES (?)', (first,))
      self.conn.commit()

   #pass

db = FormDb()
#import lock
n = 0
@app.route('/', methods=['POST'])
def on_req():
   global n
   form_db = FormDb()
   f = request.form['name']
   print(f)
   n = n + 1
   #lock.get_id(n)
   db.add_contact(f)
   return 'ok'


#l =
def test_objid():
   for i in urange(0, 1000):
      l = i
'''


