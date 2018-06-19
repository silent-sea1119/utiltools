
class FaexException(Exception):
   def __init__(self, val):
      self.parameter = val
   def __str__(self):
      return repr(self.parameter)
   #pass


