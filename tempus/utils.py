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

class Info(threading.Thread):
   pass

class Notifier(threading.Thread):
   '''
   Class to notify progress bar when time is up
   '''
   def __init__(self, duration, bar):
      threading.Thread.__init__(self)
      self._duration = duration
      self._bar = bar

   # Start timer
   def run(self):
      # Notify bar after done sleeping
      time.sleep(self._duration)
      self._bar.notify()

class Bar(object):
   '''
   Class for progress bar
   '''
   FRAME_CHAR_STAGES = {
      'block': ['\u258F', '\u258E', '\u258D', '\u258C', 
                '\u258B', '\u258A', '\u2589', '\u2588']
   }
   BORDER_CHAR = '|'
   REMAINING_CHAR = ' '

   def __init__(self, info, complete_in, 
      frame_char_type='block', length=80):
      # Bar 
      self._bar_length = length - len(info)
      # Frames
      self._total_frames = self._bar_length - 2
      self._current_frame = 1
      self._frame_stack = ''
      # Stages
      frame_stages = Bar.FRAME_CHAR_STAGES[frame_char_type]
      self._stage_in_cycle = itertools.cycle(frame_stages)
      self._last_stage = frame_stages[-1]
      # Info 
      self._info = info
      self._info_length = len(info)
      # Duration
      self._total_seconds = complete_in
      self._time_up = False
      # Gaps (In seconds)
      stages_per_frame = len(frame_stages)
      total_gaps = self._total_frames*stages_per_frame - 1
      self._normal_gap = truncate(self._total_seconds/total_gaps, 5)
      self._first_gap = \
         self._total_seconds - total_gaps*self._normal_gap + self._normal_gap

   # Get latest info
   def _get_info(self):
      info = self._info[:self._info_length]
      if len(self._info) < self._info_length:
         info += ' '*(self._info_length-len(self._info))
      return info

   # Update info
   def _update_info(self, info):
      self._info = info

   # Start progress bar
   def start(self):
      # Start notifer thread
      Notifier(self._total_seconds, self).start()
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
                  self._get_info()), end='\r', flush=True)
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
                  self._get_info()), end='\r', flush=True)     
               break          
         print()

   # Receive notification that time is up
   def notify(self):
      self._time_up = True
