

def map2(f, lst):
   return list(map(f, lst))

def myfilter2(f, lst):
   return list(filter(f, lst))



#enum class names as strings
def enum_to_lst_strs(e):
   return list(map(lambda x: x.name, e))


def flatten(lst):
   ret = []
   for x in lst:
      if type(x) is list:
         ret += flatten(x)
      else:
         ret.append(x)
   return ret

#f(data1, data2)
def map_to_list_or_item(f, data1, data2):

   '''

   map_to_list_or_item(lambda x,y: x+' '+y, 'greeting', 'bye')
      -> 'greeting bye'

   map_to_list_or_item(lambda x,y: x+' '+y, 'greeting', ['bye', 'goodnight'])
      -> ['greeting bye', 'greeting goodnight']

   map_to_list_or_item(lambda x,y: x+' '+y, ['greeting', 'hello'], 'bye')
      -> ['greeting bye', 'hello bye']

   map_to_list_or_item(lambda x,y: x+' '+y, ['hi', 'greeting'], ['bye', 'goodnight'])
      -> ['hi bye', 'hi goodnight', 'greeting bye', 'greeting goodnight']

   '''

   if type(data1) is not list and type(data2) is not list:
      return f(data1, data2)

   new_f2 = f
   if type(data2) is list:
      new_f2 = lambda arg1_, arg2_: list(map(lambda arg2: f(arg1_, arg2), arg2_))

   new_f1 = new_f2
   if type(data1) is list:
      new_f1 = lambda arg1_, arg2_: list(map(lambda arg1: new_f2(arg1, arg2_), arg1_))

   result = new_f1(data1, data2)
   ret = flatten(result)

   return ret




