

log_f = open('log.txt', 'a')
log_f.write('============running ./faex/orderbook.py\n')

def klog(*args):
   print(*args)

   log_str = ''
   for arg in args:
      log_str += str(arg)
   log_str += '\n'

   log_f.write(log_str)


