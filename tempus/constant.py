# constant.py
# Global constants 

# Strings
VERSION = '1.1.0'
DURATION_REGEX = '^(([0-9]+)m)?(([0-9]+)s)?$'
FRAME_CHAR_STAGES = {
   'block': [' ', '▏', '▎', '▍', '▌', '▋', '▊', '▉', '█'],
   'dots': ['⡀', '⡄', '⡆', '⡇', '⣇', '⣧', '⣷', '⣿']
}
BORDER_CHAR = '|'
REMAINING_CHAR = ' '

# Numbers
TERMINAL_DEFAULT_SIZE = (80, 25)
TERMINAL_MINIMUM_SIZE = (80 ,10)
