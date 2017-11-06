# utils.py
# Utility functions

import itertools
import cursor
import time

def progress_bar(initial_info='', bar_type='rectangle', length=80, 
   complete_in=0):
   '''
   usage:
      loading = itertools.cycle(['Loading.', 'Loading..', 'Loading...'])
      for frame in progress_bar('Loading'):
         frame.update_info(next(loading))
         time.sleep(0.25)
   '''

   # |############| Running...
   # bar------------info------
   #  frame-------

   # Class for progress bar to keep info updated by caller
   class Info:
      def __init__(self, info, cutoff):
         self._info = info
         self._cutoff = cutoff
      def get_info(self):
         info = self._info[:self._cutoff]
         if len(self._info) < self._cutoff:
            info += ' '*(self._cutoff-len(self._info))
         return info
      def update_info(self, info):
         self._info = info
   info = Info(initial_info, len(initial_info))

   info_length = len(initial_info)
   bar_length = length - info_length

   # Stages for a bar frame to become full or complete
   bar_stages = {
      'rectangle': ['\u258F', '\u258E', '\u258D', '\u258C', 
                    '\u258B', '\u258A', '\u2589', '\u2588']
   }
   stage = itertools.cycle(bar_stages[bar_type])
   last_stage = bar_stages[bar_type][-1]

   border_char = '|'
   remaining_char = ' '
   gap_char = ' '
   total_frames = bar_length - 3
   current_frame = 1
   frame_stack = ''

   time_constraint = False
   if complete_in >= 0:
      time_constraint = True
      total_seconds = complete_in
      number_of_stages = len(bar_stages[bar_type])
      total_stages = total_frames * number_of_stages 
      seconds_per_stage = total_seconds / total_stages

   # Yield progress bar stage by stage
   with cursor.HiddenCursor():
      while current_frame <= total_frames:
         remaining_frames = total_frames - current_frame
         current_stage = next(stage)
         print(
            border_char +
            frame_stack + 
            current_stage +
            remaining_char*remaining_frames +
            border_char + 
            gap_char +
            info.get_info() \
            , end='\r', flush=True)
         yield info
         time.sleep(seconds_per_stage)
         # Update frame stack when the current frame is complete
         if current_stage == last_stage:
            frame_stack += last_stage
            # Move on to next frame
            current_frame += 1 
   print()