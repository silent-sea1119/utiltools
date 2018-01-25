
class Event(object):
   def __init__(self, init_handler=None):
      super(Event, self).__init__()
      self._signals = list()
      self.add(init_handler)
      #pass

   def add(self, handler):
      if handler is not None:
         self._signals.append(handler)
      #pass

   def remove(self, handler):
      if handler in self._signals:
         self._signals.remove(handler)
      #pass

   def __call__(self, *args, **kwargs):
      for handler in self._signals:
         if handler is not None:
            handler(*args, **kwargs)
      #pass

   def __contains__(self, item):
      return item in self._signals

   def __iadd__(self, other):
      self.add(other)
      return self

   def __isub__(self, other):
      self.remove(other)
      return self

   #pass

####
#e = Event()
#def f....
#e += f
#e()

