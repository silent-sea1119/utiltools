
import sqlite3, os.path, json
#from flask import Flask, request, send_from_directory

#from . import dbhelpers, atomicid

#app = Flask(__name__)
#DB_PATH = '/tmp/permtest.db'

######################Perm
#perms are asrw, a being (a)dministrator privelages (can give out read/write), and s is (s)uper admin which can give out admin and superadmin
#perms = Perm([Perm.ADMIN, Perm.SUPER, Perm.READ, Perm.WRITE])

#x = Perm([Perm.ADMIN, Perm.SUPER])
#x = Perm(0 | Perm.ADMIN | Perm.SUPER)
#x = Perm('asrw')
#x = Perm(Perm.ADMIN)

#x = Perm(Perm.ADMIN | Perm.WRITE)
#y = Perm(x)
#z = Perm(y.val | Perm.WRITE) #new perm z with same permissions as y, plus write

#x.get_status() == 0
#x.has_read(), x.has_write(), x.has_admin(), x.has_super_admin()

######################

class Perm(object):
   '''Permission

   ``perms = Perm([Perm.ADMIN, Perm.SUPER, Perm.READ, Perm.WRITE])``

   ``x = Perm(Perm.ADMIN | Perm.WRITE)``

   ``x.get_status() == 0``

   ``x.has_read(), x.has_write(), x.has_admin(), x.has_super_admin()``


   '''

   ADMIN = (1 << 0)
   SUPER = (1 << 1)
   READ = (1 << 2)
   WRITE = (1 << 3)
   _ALL_ARR = [ADMIN, SUPER, READ, WRITE]

   def save_arr(self, arr):
      self.val = 0
      for x in arr:
         if x not in Perm._ALL_ARR:
            return 1
         self.val = self.val | x

      if not self.check_num_valid(self.val):
         return 3
      return 0

   def save_str(self, string):
      self.val = 0

      good = list('asrw')
      for c in string:
         if c not in good:
            return 1
         if c == 'a':
            self.val = self.val | Perm.ADMIN
         elif c == 's':
            self.val |= Perm.SUPER
         elif c == 'r':
            self.val |= Perm.READ
         elif c == 'w':
            self.val |= Perm.WRITE

      if not self.check_num_valid(self.val):
         return 3
      return 0

   # check_num_valid: checks raw value of self.val
   # self.val is underlying format for storage of permission
   # valid = True, invalid = False
   def check_num_valid(self, n):
      if n is None:
         return False
      all_perms = 0
      for x in Perm._ALL_ARR:
         all_perms |= x
      if (n | all_perms) != all_perms:
         return False
      return True

   def save_copy(self, perm_copy):
      if not self.check_num_valid(perm_copy.val):
         return 3
      self.val = perm_copy.val
      return 0

   def save_num(self, n):
      if not self.check_num_valid(n):
         return 3
      self.val = n
      return 0

   #get_status(): call after init, returns status of initialization
   #-1 = uninitialized status, 0 = success
   #1 = one of characters in string or items in array is invalid
   #2 = invalid data type passed to constructor. Can only be list, str, int or Perm
   #3 = check_num_valid() returned False. mostly means that save_copy or save_num got bad data, but also
   #    used in save_str and save_arr
   #4 = uninitialized val
   def get_status(self):
      return self.status

   def __init__(self, item):
      self.status = -1
      self.val = None

      if type(item) is list: #list of Perm objects
         self.status = self.save_arr(item)
      elif type(item) is str: #string format
         self.status = self.save_str(item)
      elif type(item) is Perm: #other perm or one of the capital constants
         self.status = self.save_copy(item)
      elif type(item) is int:
         self.status = self.save_num(item)
      else:
         self.status = 2

      if  self.val is None and (self.status == -1 or self.status == 0):
         self.status = 4

      pass #end __init__()

   def has_read(self):
      '''Has read'''
      return (self.val & Perm.READ) is not 0
   def has_write(self):
      '''Has write'''
      return (self.val & Perm.WRITE) is not 0
   def has_admin(self):
      '''Has admin'''
      return (self.val & Perm.ADMIN) is not 0
   def has_super_admin(self):
      '''Has super admin'''
      return (self.val & Perm.SUPER) is not 0

   #pass #end class Perm


