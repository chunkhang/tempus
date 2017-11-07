from click import command, argument
import cursor
import time
import re
import sys
import datetime
import threading
import itertools

from ..utils import truncate

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
   bar = Bar(10)
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

class Bar(object):
   '''
   Class for progress bar
   '''
   class Timer(threading.Thread):
      '''
      Class to update time remaining
      '''
      def __init__(self, starting_seconds):
         threading.Thread.__init__(self)
         self._remaining_seconds = starting_seconds
      # Convert seconds to string
      def _to_string(seconds):
         m, s = divmod(seconds, 60)
         return '{}:{:02d}'.format(m, s)
      # Start counting down
      def run(self):
         while self._remaining_seconds > 0:
            time.sleep(1)
            self._remaining_seconds -= 1
      # Get current time
      def get_current_time(self):
         return Bar.Timer._to_string(self._remaining_seconds)
      def get_zero_time(self):
         return Bar.Timer._to_string(0)

   FRAME_CHAR_STAGES = {
      'block': ['\u258F', '\u258E', '\u258D', '\u258C', 
                '\u258B', '\u258A', '\u2589', '\u2588']
   }
   BORDER_CHAR = '|'
   REMAINING_CHAR = ' '

   def __init__(self, duration, frame_char_type='block', length=80):
      # Duration
      self._total_seconds = duration
      self._timer = Bar.Timer(duration)
      self._time_up = False
      # Frames
      self._total_frames = length - 2 - len(self._timer.get_current_time())
      self._current_frame = 1
      self._frame_stack = ''
      # Stages
      frame_stages = Bar.FRAME_CHAR_STAGES[frame_char_type]
      self._stage_in_cycle = itertools.cycle(frame_stages)
      self._last_stage = frame_stages[-1]
      # Gaps (In seconds)
      stages_per_frame = len(frame_stages)
      total_gaps = self._total_frames*stages_per_frame - 1
      self._normal_gap = truncate(self._total_seconds/total_gaps, 5)
      self._first_gap = \
         self._total_seconds - total_gaps*self._normal_gap + self._normal_gap

   # Receive notification that time is up
   def _notify(self):
      self._time_up = True

   # Start progress bar
   def start(self):
      # Start timer thread
      self._timer.start()
      # Start notifier thread
      # Notify that time is up after duration expires
      threading.Timer(self._total_seconds, lambda: self._notify()).start()
      with cursor.HiddenCursor():
         first_stage_now = True
         remaining_frames = self._total_frames - self._current_frame
         while self._current_frame <= self._total_frames:
            # Add frames stage by stage smoothly, if there is still time
            if not self._time_up:
               # Sleep between stages
               if first_stage_now:
                  time.sleep(self._first_gap)
                  first_stage_now = False
               else:
                  time.sleep(self._normal_gap)
               # Update bar
               current_stage = next(self._stage_in_cycle)
               print('{}{}{}{}{}{}'.format(
                  Bar.BORDER_CHAR, 
                  self._frame_stack,
                  current_stage,
                  Bar.REMAINING_CHAR*remaining_frames,
                  Bar.BORDER_CHAR,
                  self._timer.get_current_time()), end='\r', flush=True)
               # Update frame stack when the current frame is complete
               # Move on to next frame
               if current_stage == self._last_stage:
                  self._frame_stack += self._last_stage
                  self._current_frame += 1
                  remaining_frames -= 1
            # Fill in remaining frames immediately, if time is up
            else:
               print('{}{}{}{}'.format(
                  Bar.BORDER_CHAR, 
                  self._last_stage*self._total_frames,                  
                  Bar.BORDER_CHAR,
                  self._timer.get_zero_time()), end='\r', flush=True)     
               break          
         print()