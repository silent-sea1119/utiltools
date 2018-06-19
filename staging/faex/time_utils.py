
import datetime as dt
from datetime import datetime as dt2
import time

MICROS_IN_SEC = 1000000

def read_dt_from_str(dt_str, format_str=None):
   if format_str is None:
      format_str = '%Y-%m-%dT%H:%M:%S.%fZ'

   return dt2.strptime(dt_str, format_str)

def dt_to_tstamp(dt):
   return time.mktime(dt.timetuple())

def str_to_tstamp_no_micro(dt_str):
   return dt_to_tstamp(read_dt_from_str(dt_str))

def str_to_tstamp_micro(dt_str, is_float=True):
   '''If is_float = True, return in seconds with micro as decimal.
   If is_float = False, return in microseconds int'''
   ret = read_dt_from_str(dt_str).timestamp()
   if not is_float:
      ret *= MICROS_IN_SEC #mill
      ret = int(ret)
   return ret

def micro_tstamp_to_dt(micro_tstamp):
   sec_tstamp = micro_tstamp / MICROS_IN_SEC
   return dt2.fromtimestamp(sec_tstamp)


