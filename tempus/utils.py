# utils.py
# Utility functions

import math
import os
import shlex
import struct
import platform
import subprocess

from . import constant

def truncate(float_number, decimal_point):
   '''
   e.g. _truncate(1.67592, 3) -> 1.675
   '''   
   magic_number = 10 ** decimal_point
   return math.floor(float_number*magic_number) / magic_number

def terminal_size(_default=constant.TERMINAL_DEFAULT_SIZE):
   '''
   -> (int, int): (width, height)
   Code obtained and modified from: https://gist.github.com/jtriley/1108174
   '''
   def _get_terminal_size_windows():
      try:
         from ctypes import windll, create_string_buffer
         # stdin handle is -10
         # stdout handle is -11
         # stderr handle is -12
         h = windll.kernel32.GetStdHandle(-12)
         csbi = create_string_buffer(22)
         res = windll.kernel32.GetConsoleScreenBufferInfo(h, csbi)
         if res:
            (bufx, bufy, curx, cury, wattr,
               left, top, right, bottom,
               maxx, maxy) = struct.unpack("hhhhHhhhhhh", csbi.raw)
            sizex = right - left + 1
            sizey = bottom - top + 1
            return sizex, sizey
      except:
         pass
   def _get_terminal_size_tput():
      try:
         cols = int(subprocess.check_output(shlex.split('tput cols')))
         rows = int(subprocess.check_output(shlex.split('tput lines')))
         return (cols, rows)
      except:
         pass
   def _get_terminal_size_linux():
      def ioctl_GWINSZ(fd):
         try:
            import fcntl
            import termios
            cr = struct.unpack('hh', 
               fcntl.ioctl(fd, termios.TIOCGWINSZ, '1234'))
            return cr
         except:
            pass
      cr = ioctl_GWINSZ(0) or ioctl_GWINSZ(1) or ioctl_GWINSZ(2)
      if not cr:
         try:
            fd = os.open(os.ctermid(), os.O_RDONLY)
            cr = ioctl_GWINSZ(fd)
            os.close(fd)
         except:
            pass
      if not cr:
         try:
            cr = (os.environ['LINES'], os.environ['COLUMNS'])
         except:
            return None
      return int(cr[1]), int(cr[0])
   current_os = platform.system()
   tuple_xy = None
   if current_os == 'Windows':
      tuple_xy = _get_terminal_size_windows()
      if tuple_xy is None:
         tuple_xy = _get_terminal_size_tput()
   if current_os in ['Linux', 'Darwin'] or current_os.startswith('CYGWIN'):
      tuple_xy = _get_terminal_size_linux()
   if tuple_xy is None:
      tuple_xy = _default
   return tuple_xy
