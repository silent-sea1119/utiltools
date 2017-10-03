
from utiltools.perm import Perm
#from .perm import Perm
#from .perm import UserPermissions
from . import UserPermissions
from . import atomicid
from . import dbdict

from . import secpassdb


'''Perm example
x = Perm([Perm.ADMIN, Perm.SUPER])
x = Perm('asrw')
x = Perm(Perm.ADMIN)
y = Perm(x)
'''

'''UserPermissions example

#from perm import UserPermissions
from user_acc import UserPermissions
p = UserPermissions('/sec/db/dbtnext/usertest.db')

p.new_group('viewer')
p.new_group('writer')
p.new_group('privaleged_viewer')
p.new_group('privaleged_modifier')
p.new_group('admin')

#main user
p.new_user('root')
p.new_group('root')
p.add_user_to_group('root', 'root')
p.add_user_to_group('admin', 'root')

#approve section
p.new_resource('approve_section')
p.resource_group_add_perms('approve_section', 'root', 'ws') #'ws'
p.resource_group_rm_perms('approve_section', 'admin', 'rw') #'rws'
p.resource_group_rm_perms('approve_section', 'admin', 'wa', True) #resets, so 'wa' and no 's' or 'r'

p.get_resource_group_perms('approve_section', 'root')
'''

'''
#@requires_group('admin')
@p.resource_name('approve_section')
def approve_user(uname):
   pass

#@requires_group('admin')
@p.resource_name('modify_user_group')
def add_user_to_group(uname, grp):
   pass

@p.resource_name('report')
def get_report(reportname):
   pass

#def view_report():
#   pass
'''



'''secpassdb example'''



