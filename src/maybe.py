
class Maybe:
   '''Maybe'''
   def __init__(self, val, err_code=None):
      '''Constructor takes values and err_code'''
      self.val = val
      self.err_code = err_code

   def is_good(self):
      '''Checks if err_code is None'''
      return self.err_code is None
   def is_err(self):
      return self.err_code is not None
   def get_val(self):
      return self.val
   def get_err(self):
      return self.val
   def get_err_code(self):
      return self.err_code

   def __repr__(self):
      ret = '<Maybe is_err=' + str(self.is_err()) + ' '
      if self.is_err():
         ret += ' err_code=' + str(self.err_code)
      ret += ' ret={' + repr(self.val) + '}'
      ret += '>'
      return ret

   #pass


