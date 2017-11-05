#!/usr/bin/env python3

from click import group

from .commands import *
from .commands import COMMANDS

@group()
def cli():
   pass

# Add all commands to cli
for command in COMMANDS:
   cli.add_command(getattr(locals()[command], 'execute'))

if __name__ == '__main__':
   cli()