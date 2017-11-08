from click import command, argument

from . import timer
from .. import constant

@command('test', short_help='test font suitability')
def execute(): 
   print('Ensure that the characters below are:')
   print('* Equal in height')
   print('* Forming a smooth gradient across')
   print('* Aesthetically pleasing')
   print()
   for v in constant.FRAME_CHAR_STAGES.values():
      print('{}{}{}'.format(
         constant.BORDER_CHAR,
         ''.join(reversed(v)),
         constant.BORDER_CHAR))
   print()
   print('https://github.com/chunkhang/tempus/#font')