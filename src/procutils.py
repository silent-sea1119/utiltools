
import signal, pexpect

#same as running "ps -e" from bash
#returns a list of processing where each process is a hash with pid, term, time and process name.
def gnu_ps_e():
   processes = []
   child = pexpect.spawn('ps -e', timeout=None)

   while True:
      child.expect(["(?P<pid>[0-9]+)\s+(?P<term>[^\s]+)\s+(?P<timeran>[0-9:]+)\s+(?P<pname>[^\r]*)", pexpect.EOF])
      #print(child.after)
      if child.match == pexpect.EOF:
         break
      data = child.match.groupdict()

      #next 2 lines will mess up ps
      #if not child.isalive():
      #   break

      #print(data)
      processes.append(data)
   return processes

#name or pid
def get_proc(search_by, critaria, processes=None):
   if not processes:
      processes = gnu_ps_e()

   assert logical_xor(search_by=='name', search_by=='pid')
   if search_by == 'name':
      for proc_line in processes:
         proc_line['pid'] = int(proc_line['pid'])
         if proc_line['pname'] == critaria:
            return proc_line
   if search_by == 'pid':
      for proc_line in processes:
         proc_line['pid'] = int(proc_line['pid'])
         if proc_line['pid'] == critaria:
            return proc_line
   return None

def kill_proc(proc, sig=signal.SIGINT):
   if not proc:
      return #raise Exception('trying to kill non-existing process')
   elif isinstance(proc, basestring):
      kill_proc(get_proc('name', proc), sig)
   elif isinstance(proc, (int, long)):
      os.kill(proc, sig)
   else:
      kill_proc(int(proc['pid']), sig)
      #raise Exception('bad proc type')


