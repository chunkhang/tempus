# utils.py
# Utility functions

import math

def truncate(float_number, decimal_point):
   '''
   e.g. _truncate(1.67592, 3) -> 1.675
   '''   
   magic_number = 10 ** decimal_point
   return math.floor(float_number*magic_number) / magic_number