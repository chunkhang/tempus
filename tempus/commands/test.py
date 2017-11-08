from click import command, argument

from . import timer

@command('test', short_help='test font suitability')
def execute(): 
   print('Ensure that the characters below are:')
   print('* Equal in height')
   print('* Forming a smooth gradient across')
   print('* Aesthetically pleasing')
   print()
   for v in timer.Bar.FRAME_CHAR_STAGES.values():
      print('{}{}{}'.format(
         timer.Bar.BORDER_CHAR,
         ''.join(reversed(v)),
         timer.Bar.BORDER_CHAR))
   print()
   print('Ensure that the terminal is:')
   print('* At least width 80')
   print('* At least height 10')
   print()
   print('(width, height): ({}, {})'.format(1, 2))
