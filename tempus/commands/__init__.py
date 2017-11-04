from re import match
from os import listdir
from os.path import realpath, dirname

path = dirname(realpath(__file__))
files = list(filter(lambda x: match('[a-z]+\.py', x), listdir(path)))
# For import *
__all__ = list(map(lambda x: x.strip('.py'), files))
# For entry point to access
COMMANDS = __all__