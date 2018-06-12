#from gi.repository import GObject
import queue as Queue
import time

#def _queue_call = self.add()

class WorkQueue(object):
   def __init__(self):
      super(WorkQueue, self).__init__()
      self.q = Queue.Queue()
      self._busy = False
      self.last = None

   def add(self, f, *args, **kwargs):
      self.q.put((f, args, kwargs))

   def start(self):
      if self._busy:
         print('queue: cannot start queue: ' + self.last[0].__name__)
         return
      self._busy = True
      self.tick()

   def is_busy(self):
      return self._busy

   def clear(self):
      self._busy = False
      self.q.queue.clear()
      self.last = None
      #while not self.q.empty():
      #   self.q.get()

   def queue_call(self, task, *args, **kwargs):
      if self._busy:
         print('queue: busy...' + self.last[0].__name__)
         return False
      self.q.put((task, args, kwargs))
      #if self.ileni.debug:
      #   print('queue: adding %s to execution queue ' % task.__name__)
      return True

   def undo(self):
      if self.last is None:
         print('queue: nothing to undo')
         return
      print('queue: undoing')
      self._busy = True
      new_q = Queue.Queue()
      new_q.put(self.last)
      while not self.q.empty():
         new_q.put(self.q.get())
      self.q = new_q

   def tick(self):
      if not self.q.empty():
         task, args, kwargs = self.last = self.q.get()
         #if self.ileni.debug:
         #   print('queue: executing %s' % task.__name__)
         task(*args, **kwargs)
         if self.q.empty():
            print('queue: just executed last call: %s' % task.__name__)
            self._busy = False
      elif self.q.empty():
         print('queue: cannot execute empty queue')
         self._busy = False
      #elif self.ileni.debug:
      #   print('queue: empty queue')

   def is_done(self):
      return self.q.empty()

   #pass

def main():
   #import gtk
   def msg(s): print(s)

   wq = WorkQueue()
   wq.add(msg, 'hi 2')
   wq.tick()
   msg('hi 1')
   wq.tick()
   wq.add(msg, 'bye')
   wq.tick()
   #gtk.main()

if __name__ == "__main__":
   main()

main()
