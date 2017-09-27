
import time, datetime

#AttrDict({'a': 3, 'b': 5}).a
class AttrDict(dict):
   def __init__(self, *args, **kwargs):
      super(AttrDict, self).__init__(*args, **kwargs)
	self.__dict__ = self
   #pass

#x = ObjDict(); x.a = 4; x.b = 10; x.get_as_dict()
class ObjDict:
   def __init__(self):
      pass

   def get_as_dict(self):
	return self.__dict__

   #pass


def try_to_float(s, default=None):
   try:
      return float(s)
   except:
      return default

def try_to_int(s, default=None):
   try:
      return int(s)
   except:
      return default

#enum_arg = string in enum_list or int index in enum_list
def enum_helper(enum_list, enum_arg, to_index=None):
   '''enumerate a list to/from index'''
   options = [x.lower() for x in enum_list]

   if to_index is None:
      if enum_arg is None:
         return None
      elif type(enum_arg) is str:
         to_index = True
      elif type(enum_arg) is int:
         to_index = False
      else:
         raise "Bad type passed to surveydb.utils.enum_helper(%s)" % (str(enum_arg))

   try:
      if to_index:
         return options.index(enum_arg.lower())
      else:
         return options[enum_arg]
   except Exception as e:
      pass
   return None


def datetime_to_unix(d):
   return time.mktime(d.timetuple())

def unix_to_datetime(x):
   return datetime.datetime.fromtimestamp(int(x))

def datetime_to_str(d):
   return d.strftime('%Y-%m-%d %H:%M:%S')

def rand_str(length):
   '''Generate random string'''
   import string, random
   available_chars = string.ascii_uppercase + string.digits
   return ''.join(random.choice(available_chars) for _ in range(length))


def gen_random_str(length):
   import string, random
   char_pool = string.ascii_uppercase + string.digits + string.ascii_lowercase
   return ''.join(random.choice(char_pool) for _ in range(length))




