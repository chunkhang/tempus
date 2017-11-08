# -*- coding: utf-8 -*-

from __future__ import unicode_literals
from click import command, argument
import cursor
import time
import re
import sys
import threading
import itertools

from ..utils import truncate

DURATION_REGEX = '^(([0-9]+)m)?(([0-9]+)s)?$'

@command('timer', short_help='use timer')
@argument('duration')
def execute(duration):

   # Check duration syntax
   if _syntax_valid(duration):
      # Check duration values
      duration = _to_duration(duration)
      if not _values_valid(duration):
         print('Invalid duration.')
         print('Examples: 2m59s, 40m0s, 0m10s')
         sys.exit()
   else:
      print('Invalid syntax.')
      print('Examples: 10s, 5m, 20m30s')
      sys.exit()      

   # Start timer bar
   input('[Enter to start]')
   print()
   Bar(_to_seconds(duration)).start()
   print()

   # Ring bell
   _ring_bell('[Ctrl-C to stop]')
   sys.exit()
   

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
   # Seconds only
   elif m is None:
      if s == 0:
         return False
   return True

def _to_seconds(d):
   '''
   Convert duration string to seconds
   -> int: total seconds 
   '''
   m, s = d
   m = 0 if m is None else m
   s = 0 if s is None else s
   return m*60 + s

class Bar(object):
   '''
   Class for progress bar
   '''

   class Updater(threading.Thread):
      '''
      Class to continuously update bar until done
      '''
      def __init__(self, bar, timer):
         threading.Thread.__init__(self)
         self._bar = bar
         self._timer = timer
         self._stop_now = False
      def run(self):
         last = False
         while True:
            if self._stop_now:
               break
            if self._bar._get_done():
               last = True
            bar = self._bar._get_bar()
            time = self._timer.get_current_time() if not last else \
               self._timer.get_zero_time()
            sys.stdout.write('{}{}{} {} {}'.format(
               Bar.BORDER_CHAR, 
               bar,
               Bar.BORDER_CHAR,
               time,
               Bar.BORDER_CHAR))
            sys.stdout.write('\r')
            sys.stdout.flush()
            if last:
               sys.stdout.write('\n')
               sys.stdout.flush()
               break
      def stop(self):
         self._stop_now = True

   class Timer(threading.Thread):
      '''
      Class to update time remaining
      '''
      def __init__(self, starting_seconds, bar):
         threading.Thread.__init__(self)
         self._initial_length = 0
         self._initial_length = len(self._to_string(starting_seconds))
         self._remaining_seconds = starting_seconds
         self._bar = bar
         self._stop_now = False
      # Convert seconds to string
      def _to_string(self, seconds):
         m, s = divmod(seconds, 60)
         time_string = '{}:{:02d}'.format(m, s)
         if self._initial_length == 0:
            return time_string
         else:
            return time_string.rjust(self._initial_length)
      # Start counting down
      def run(self):
         while self._remaining_seconds > 0:
            if self._stop_now:
               break
            time.sleep(1)
            self._remaining_seconds -= 1
         self._bar.notify()
      def stop(self):
         self._stop_now = True
      def get_current_time(self):
         return self._to_string(self._remaining_seconds)
      def get_zero_time(self):
         return self._to_string(0)

   FRAME_CHAR_STAGES = {
      'block': [' ', '▏', '▎', '▍', '▌', '▋', '▊', '▉', '█'],
      'dots': ['⡀', '⡄', '⡆', '⡇', '⣇', '⣧', '⣷', '⣿']
   }
   BORDER_CHAR = '|'
   REMAINING_CHAR = ' '

   def __init__(self, duration, frame_char_type='block', length=80):
      threading.Thread.__init__(self)
      # Duration
      self._timer = Bar.Timer(duration, self)
      self._total_seconds = duration
      self._time_up = False
      self._done = False
      # Frames
      self._updater = Bar.Updater(self, self._timer)
      self._total_frames = length - 5 - len(self._timer.get_current_time())
      self._current_frame = 1
      self._frame_stack = ''
      self._bar = Bar.REMAINING_CHAR*self._total_frames
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

   # Return complete bar for updater
   def _get_bar(self):
      return self._bar

   # Return done status
   def _get_done(self):
      return self._done

   # Start progress bar
   def start(self):
      with cursor.HiddenCursor():
         first_stage_now = True
         remaining_frames = self._total_frames - self._current_frame
         try:
            # Start timer and updater threads
            self._timer.start()
            self._updater.start()
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
                  self._bar = self._frame_stack + current_stage + \
                     Bar.REMAINING_CHAR*remaining_frames
                  # Update frame stack when the current frame is complete
                  # Move on to next frame
                  if current_stage == self._last_stage:
                     self._frame_stack += self._last_stage
                     self._current_frame += 1
                     remaining_frames -= 1
               # Fill in remaining frames immediately, if time is up
               else:
                  self._bar = self._last_stage*self._total_frames
                  break
            self._done = True
         except KeyboardInterrupt:
            # Stop threads
            self._timer.stop()
            self._updater.stop()
            sys.exit()
         # Wait for threads to finish
         self._timer.join()
         self._updater.join()

   # Receive notification that time is up
   def notify(self):
      self._time_up = True

def _ring_bell(message, frequency=0.5):
   def _beep():
      print('\a', end='', flush=True)
   first_ring = True
   while True:
      try:
         if first_ring:
            print(message, end='')
            first_ring = False
         _beep()
         time.sleep(frequency)
      except KeyboardInterrupt:
         print()
         break