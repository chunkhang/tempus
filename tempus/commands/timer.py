from click import command, argument
import cursor
import time
import re
import sys
import datetime

from ..utils import Bar

DURATION_REGEX = '^(([0-9]+)m)?(([0-9]+)s)?$'

@command('timer', short_help='use timer')
@argument('duration')
def execute(duration):

   duration_string = duration

   # Check duration syntax
   if _syntax_valid(duration_string):
      # Check duration values
      duration = _to_duration(duration_string)
      if not _values_valid(duration):
         print('Invalid duration.')
         print('Examples: 2m59s, 40m0s, 0m10s')
         sys.exit()
   else:
      print('Invalid syntax.')
      print('Examples: 10s, 5m, 20m30s')
      sys.exit()      

   start = datetime.datetime.now()
   bar = Bar('Loading...', 10)
   bar.start()
   end = datetime.datetime.now()
   print('Elapsed: {}'.format(end-start))



   # Get total seconds
   duration = _safe_duration(duration)
   total_seconds = duration[0]*60 + duration[1]

   # # Countdown
   # print(_time_box(total_seconds))
   # message = 'Enter to start. Ctrl-C to stop.'
   # input(message)
   # print('', end='\r\033[4A')
   # stopped = False
   # with cursor.HiddenCursor(): 
   #    for i in range(int(total_seconds), 0, -1):
   #       try:
   #          print(_time_box(i))
   #          print(' '*len(message))
   #          time.sleep(1)
   #       except KeyboardInterrupt:
   #          stopped = True
   #          break
   #       finally:
   #          print('', end='\r\033[4A')
   # # Done countdown
   # if not stopped:  
   #    print(_time_box(0))
   #    _notify()
   # else:
   #     print('\n'*2)
   # print('Stopped.'+' '*len(message))
   

def _syntax_valid(ds, r=DURATION_REGEX):
   '''
   -> boolean: True - valid syntax
   -> boolean: False - invalid syntax
   '''
   m = re.compile(r).match(ds)
   if m:
      return True
   else:
      return False

def _to_duration(ds, r=DURATION_REGEX):
   '''
   -> tuple: (int/None, int/None) - (minutes, seconds)
   '''
   g = re.compile(r).match(ds).groups()
   m = int(g[1]) if g[1] is not None else None
   s = int(g[3]) if g[3] is not None else None
   return (m, s)

def _values_valid(d):
   '''
   -> boolean: True - valid duration
   -> boolean: False - invalid duration
   '''
   m, s = d
   # No minutes and seconds
   if m is None and s is None:
      return False
   # Minutes and seconds
   if m is not None and s is not None:
      if (m == 0 and s == 0) or \
         (s >= 60):
         return False
   # Minutes only
   elif s is None:
      if m == 0:
         return False
   # s only
   elif m is None:
      if s == 0:
         return False
   return True

def _safe_duration(d):
   '''
   Duration returned is guranteed to be ints, where seconds >= 0 and < 60
   -> tuple: (int, int) - (minutes, seconds)
   '''
   m, s = d
   m = 0 if m is None else m
   s = 0 if s is None else s
   total_s = m*60 + s
   m, s = divmod(total_s, 60)
   return (m, s)

def _time_string(total_s):
   '''
   -> string - mm:ss
   '''
   m, s = divmod(total_s, 60)
   return '{}:{:02d}'.format(m, s)

def _notify():
   def _beep():
      print('\a', end='', flush=True)
   message = 'Ctrl-C to stop.'
   print(message)
   while True:
      try:
         _beep()
         time.sleep(0.5)
      except KeyboardInterrupt:
         print('', end='\r\033[1A')
         break
