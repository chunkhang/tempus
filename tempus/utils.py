# utils.py
# Utility functions

import itertools
import cursor
import time
import math
import threading

def truncate(float_number, decimal_point):
   '''
   e.g. _truncate(1.67592, 3) -> 1.675
   '''   
   magic_number = 10 ** decimal_point
   return math.floor(float_number*magic_number) / magic_number



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
      def get_time(self):
         return Bar.Timer._to_string(self._remaining_seconds)

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
      self._total_frames = length - 2 - len(self._timer.get_time())
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
                  self._timer.get_time()), end='\r', flush=True)
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
                  self._timer.get_time()), end='\r', flush=True)     
               break          
         print()
