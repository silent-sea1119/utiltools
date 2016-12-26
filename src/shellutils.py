import os, os.path, importlib, json, sys, tempfile
import shutil, signal, subprocess, platform
from functools import wraps

if platform.system() == 'Linux':
   import pwd, getpass, grp
from multiprocessing import Process

#wrapper for only first argument path
def expandhome1(func):
   @wraps(func)
   def wrapper(path, *args, **kwargs):
      return func(expanduser(path), *args, **kwargs)
   return wrapper

#wrapper for every argument
def expandhome(func):
   @wraps(func)
   def wrapper(*args, **kwargs):
      new_args = []
      for arg in args:
         if arg is not None:
            new_args.append(expanduser(arg))
         else:
            new_args.append(arg)
      new_kwargs = {}
      for key in kwargs:
         if kwargs[key] is not None:
            new_kwarg[key] = expanduser(kwargs[key])
         else:
            new_kwargs[key] = kwargs[key]
      return func(*new_args, **new_kwargs)
   return wrapper

@expandhome
def mkdir(path):
   """recursively create dirs (like mkdir -p). Expands home (~)

   :param   path: Path to directory to create
   :type    path: str
   """
   #os.mkdir(name) #make one directory
   #exists_ok prevents errors when dir already exists
   os.makedirs(path, exist_ok=True)

@expandhome
def ls(path='.'):
   """List files in current directory (default is current directory). Expands home (~)

   :param   path: Path to to list directories
   :type    path: str
   """
   return os.listdir(path)

@expandhome
def is_file(path):
   """Check if given path is a file. Expands home (~)"""
   return os.path.isfile(path)

@expandhome
def is_dir(path):
   """Checks if given path is a directory. Expands home"""
   return os.path.isdir(path)

@expandhome
def is_link(path):
   """Check if given path is a link. Expands home"""
   return os.path.islink(path)

@expandhome
def is_mount_point(path):
   """Check if given path is a mount point. Expands home"""
   return os.path.ismount(path)

@expandhome
def get_file_types(path):
   types = []
   if is_file(path):
      types.append('file')
   if is_dir(path):
      types.append('dir')
   if is_link(path):
      types.append('link')
   if is_mount_point(path):
      types.append('mount point')
   return types

#helper rm function
@expandhome1
def _rm_single(path, ignore_errors=False):
   """Helper function shouldn't be used outside library."""
   if is_dir(path):
      #os.removedirs(path) #only works for empty
      shutil.rmtree(path, ignore_errors=ignore_errors)
   elif is_file(path) or is_link(path):
      try:
         os.remove(path)
      except Exception as e:
         if not ignore_errors:
            raise e
   else:
      if file_exists(path) and not ignore_errors:
         raise Exception('Trying to remove unknown file type')
      else:
         pass #trying to remove non-existant path

#@expandhome
def rm(*paths, ignore_errors=False):
   """Removes files and directories. Expands home"""
   for path in paths:
      _rm_single(path, ignore_errors)

@expandhome
def cp(src, dst):
   """Copies file or directory recursively. Expands home"""
   if is_dir(src):
      shutil.copytree(src, dst)
   elif is_file(src):
      shutil.copy(src, dst)

@expandhome
def mv(src, dst):
   """Moves a file or directory. Expands home"""
   shutil.move(src, dst)

@expandhome
def ln(target, name):
   """Creates symbolic link. Expands home"""
   os.symlink(target, name)

#http://stackoverflow.com/a/13197763
@expandhome
def cd(path):
   """Changes directory. Expands home"""
   os.chdir(path)

class cd_:
    """Context manager for changing the current working directory"""
    def __init__(self, newPath):
        self.newPath = os.path.expanduser(newPath)

    def __enter__(self):
        self.savedPath = os.getcwd()
        os.chdir(self.newPath)

    def __exit__(self, etype, value, traceback):
        os.chdir(self.savedPath)

##PATH STUFF
def cwd():
   """Get current working directory."""
   return os.getcwd()

def join(*args):
   """Same as os.path.join."""
   return os.path.join(*args)

def expanduser(path):
   """Expands ~ and %HOME% into full path."""
   return os.path.expanduser(path)

#TODO: kk Something bad here
@expandhome
def expand_link(path):
   return os.path.realpath(path)

#dirname(f) gets directory path of f, doesn't work for relative path
@expandhome
def get_file_dir(path):
   return os.path.dirname(path)

#gets the name of file given path
@expandhome
def get_file_name(path):
   return os.path.basename(path)

#os.path
#expanduser() = fixes ~
#realpath(path) removes symbolic links, and if file relative, add absolute path
   #cwd = '/test/blah' #blah has file called test
   #realpath('test') => 'test/blah/test'
#normpath(path) 'A//B', 'A/B/', 'A/foo/../B' => 'A/B'
#abspath(path) same as normpath but also prepends cwd()
#kinda same as normpath(join(os.getcwd(), path))

#say you have app/src/main.py. To get path of project directory (app)
#from main.py you can use get_relative_path(__file__, '..')
@expandhome
def get_abs_path_relative_to(current_file, *relative_path):
   from os.path import abspath, dirname, realpath, join
   if relative_path is None:
      relative_path = ['']
   return abspath(join(dirname(realpath(current_file)), *relative_path))

@expandhome
def check_paths(*paths):
   """Returns list of given paths that don't exist. Expands home"""
   bad = []
   for p in paths:
      if file_exists(p) is False:
         bad.append(p)
   return bad
##END OF RANDOM PATH STUFF

@expandhome
def file_exists(filePath):
   """Checks if path exists in the system. Expands home"""
   return (filePath is not None) and os.path.exists(filePath)

@expandhome1
def write_file(filePath, data, binary=False):
   """Writes data to file. Expands home"""
   flags = 'w'
   if binary:
      flags = 'wb'
   with open(filePath, flags) as f:
      return f.write(data)

@expandhome1
def read_file(filePath, nBytes=None, binary=False, createIfNeeded=False):
   """Read data from file. Expands home"""
   if file_exists(filePath):
      # FIXISSUE: where encoding error breaks updater flow
      errors = 'replace'
      flags = 'r'
      if binary:
         errors = None # FIXISSUE: remove encoding error replacement on binary data
         flags = 'rb'
      with open(filePath, flags) as f:
         if nBytes:
            return f.read(nBytes)
         else:
            return f.read()
   elif filePath and createIfNeeded:
      assert not nBytes
      file(filePath, 'w').close()
   return None

@expandhome1
def write_json(path, json_data):
   """Writes given json object to a file. Expands home"""
   write_file(path, json.dumps(json_data) + '\n')

@expandhome1
def read_json(path):
   """Reads a file and returns it as json object. Expands home"""
   if path:
      data = read_file(path)
      if data:
         return json.loads(data)
   return None

@expandhome1
def get_file_size(filename):
   """Get the file size by seeking end. Expands home"""
   fd = os.open(filename, os.O_RDONLY)
   try:
      return os.lseek(fd, 0, os.SEEK_END)
   finally:
      os.close(fd)
   return -1

def parse_mtab():
   """Parses mtab and returns it as a list of dictionaries. Linux only."""
   mounts = []
   mtab_str = read_file('/etc/mtab').strip()
   entries = mtab_str.split('\n')
   for entry in entries:
      lst = entry.split(' ')
      #http://serverfault.com/questions/267609/how-to-understand-etc-mtabm
      item = {
         'mount-device'    : lst[0], #current device in /dev/sd*[n]
         'mount-point'     : lst[1], #where it's mounted
         'file-system'     : lst[2],
         'mount-options'   : lst[3],
         'dump-cmd'        : lst[4],
         'fsck-order-boot' : lst[5]
      }
      mounts.append(item)
   return mounts

#works for drives and partitions
def get_mount_point(drive):
   """Gets mount point of given drive."""
   mounts = parse_mtab()
   for device in mounts:
      if device['mount-device'] == drive:
         return device['mount-point']
   return None

#new thread non-block
def func_thread(callback):
   p = Process(target=callback).start()

#non-blocking
def exec_prog(command):
   if type(command) is list:
      args = command
   else:
      args = command.split()
   p = Process(target=lambda:subprocess.call(args))
   p.start()

def exec_sudo(cmd):
   return exec_get_stdout('gksudo %s' % cmd)

#TODO: use arrays instead of map/dict?
def exec_prog_with_env(command, envBindings):
   args = command.split()
   my_env = os.environ.copy() #vs os.environ
   for name in envBindings:
      my_env[name] = envBindings[name]

   def subProc():
      #TODO: why shell == True???
      subprocess.Popen(args, env=my_env, shell=True)

   Process(target=subProc).start()


#blocking, returns output
def exec_get_stdout(command):
   args = command.split()
   task = subprocess.Popen(args, stdout=subprocess.PIPE)
   return task.communicate()

#pip install sh
#http://plumbum.readthedocs.org/en/latest/index.html
def exec_bash(command):
   os.system(command)

def get_random_byte_str(length=15):
   return read_file('/dev/urandom', length, binary=True)

#TODO: maybe replace with python version
def get_random(max_num=None, min_num=0):
   rand_len = get_random_byte_str(1)[0] % 10 + 1
   rand_str = get_random_byte_str(rand_len)
   total = 0
   i = 1
   for x in rand_str:
      total += x * i
      i*= 10
   min_ = 0
   if max_num is None:
      return total + min_num
   return (total % (max_num + 1)) + min_num

##group and passwd stuff
#TODO: add stuff for making groups, adduser,
#useradd, add user to groups, etc.

def chmod():
   pass
   #TODO: http://www.tutorialspoint.com/python/os_chmod.htm
   #http://stackoverflow.com/questions/12791997/how-do-you-do-a-simple-chmod-x-from-within-python
   #https://docs.python.org/2/library/stat.html#stat.S_ISUID

def chown(path, uid, gid):
   """Change owner and group of a file."""
   os.chown(path, uid, gid)

def get_current_user_id():
   return os.getuid()

def is_admin():
   return get_current_user_id() == 0

def get_current_user_name():
   return getpass.getuser()

def get_user_info(usrname=None, usrid=None):
   info = None
   if usrname is not None and usrid is not None:
      msg = "Calling get_user_info with usrid and usrname but only 1 allowed"
      raise Exception(msg)
   if usrname is not None:
      info = pwd.getpwnam(usrname)
   elif usrid is not None:
      info = pwd.getpwuid(usrid)
   else:
      info = pwd.getpwuid(get_current_user_id())
   return info

def get_user_id(usrname=None, usrid=None):
   return get_user_info(usrname, usrid)[2]
def get_user_group_id(usrname=None, usrid=None):
   return get_user_info(usrname, usrid)[3]
def get_user_home_dir(usrname=None, usrid=None):
   return get_user_info(usrname, usrid)[5]
def get_user_shell(usrname=None, usrid=None):
   return get_user_info(usrname, usrid)[6]

#unix user groups
def get_group_db():
   return grp.getgrall()

def get_group_by_name(name, grpdb=None):
   """Given name of group, return it's internal structure."""
   if grpdb is None:
      grpdb = get_group_db()
   for group in grpdb:
      if group.gr_name == name:
         return group
   return None

def get_name_from_group_data(groupdata):
   """Given internal groupdata, get group's name."""
   return groupdata.gr_name

#TODO: check if both are none
#TODO: check if get_group_by_name returns None
def get_group_members(groupname=None, groupdata=None):
   """Returns list of user names in the given group name or group_data that was obtained from get_group_by_name()."""
   if groupdata is None:
      groupdata = get_group_by_name(groupname)
   return groupdata.gr_mem

def get_user_groups(usrname, grpdb=None):
   """Returns list of group names that the user is member of."""
   ret = []

   if grpdb is None:
      grpdb = get_group_db()
   for group in grpdb:
      members = get_group_members(groupdata=group)
      for grp_mem in members:
         if grp_mem == usrname:
            ret.append(get_name_from_group_data(group))
   return ret

def get_password_db():
   """Returns password database"""
   return pwd.getpwall()
#end pwd

def ver_lst_to_str(ver):
   s = ''
   for x in ver:
      s += '.%i' % x
   return s[1:]

def ver_str_to_lst(ver):
   s = ver.split('.')
   return list(map(int, s.split('.')))

def normalize_version(ver, length=4):
   """Takes version as a list and how long it should be.
      Appends 0's if it's not long enough."""
   if len(ver) > length:
      raise Exception('Version is longer than the longest length')
   return ver + ([0] * (length - len(ver)))

def reload_module(module):
   """from pycloak import shellutils. shellutils.reload_module(shellutils)"""
   importlib.reload(module)

def recompile_pycloak(m=None, pycloak_path='~/work/pycloak'):
   """Recompile and import module. Useful for quick command line testing without re-starting repl."""
   import sh
   current_path = cwd()

   pycloak_path = expanduser(pycloak_path)
   cd(pycloak_path)
   sh.make()
   sh.make('install')
   cd(current_path)
   if m is not None:
      reload_module(m)

@expandhome
def if_exists_append_copy(path):
   """f('test.py') = if not exists, return path, otherwise test-copy-0.py
                     if test-copy-0.py exists, return test-copy-1.py
   """
   if file_exists(path):
      path_before_ext, ext = os.path.splitext(path)
      splitted = path_before_ext.split('-')
      already_copy = False
      if len(splitted) > 2 and splitted[-1].isdigit() and splitted[-2] == 'copy':
         already_copy = True
      ret_str = ''
      if not already_copy:
         ret_str = "%s%s%s" % (path_before_ext, '-copy-0', ext)
      else:
         first_part = '-'.join(splitted[0:-2])
         ret_str = "%s%s%i%s" % (first_part, '-copy-', int(splitted[-1])+1, ext)
      return if_exists_append_copy(ret_str)
   return path

def tmp_folder(prefix='tmp', suffix=''):
   """Returns path to temporary folder with prefix and suffix."""
   return tempfile.mkdtemp(suffix, prefix)

class ProgressBar(object):
    """Progress bar for terminal."""
    def __init__(self, max_width = 20):
        self.spinner = ['/', '-', '\\', '-']
        self.spinner_tick = 0
        self.max_width = max_width

    def update(self, p, label=""):
        """Update progress with optional label"""
        tw,th = shutil.get_terminal_size(fallback=(80,40))
        self.spinner_tick += 1
        i = int((p * self.max_width) / 100)
        s = self.spinner[self.spinner_tick % len(self.spinner)]
        bar = "%s%s%s" % ("".join(['='] * i), s, "".join([' '] * (self.max_width - i - 1)))
        out = "\r[%s] %s" % (bar, label)
        pad = "".join([" "] * (tw - len(out)))
        sys.stdout.write("%s%s" % (out, pad))
        sys.stdout.flush()


