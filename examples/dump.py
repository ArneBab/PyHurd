#!/usr/bin/env python
# -*- coding: utf-8 -*-

'''
dump.py - Dump a file to stdout in a "pyhurdish" way.
Copyright (C) 2008 Anatoly A. Kazantsev

This program is free software; you can redistribute it and/or modify
it under the terms of the GNU General Public License as published by
the Free Software Foundation; either version 2 of the License, or
(at your option) any later version.

This program is distributed in the hope that it will be useful,
but WITHOUT ANY WARRANTY; without even the implied warranty of
MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
GNU General Public License for more details.

You should have received a copy of the GNU General Public License along
with this program; if not, write to the Free Software Foundation, Inc.,
51 Franklin Street, Fifth Floor, Boston, MA 02110-1301 USA.
'''

import sys

from pyhurd.glibc import file_name_lookup
from pyhurd.fcntl import O_READ
from pyhurd.mach import MACH_PORT_NULL

def main (args):

  if not len (args) == 2:
    print 'Usage: %s <filename>' % args[0]
    return

  # Open file
  f = file_name_lookup (args[1], O_READ, 0)

  if f is MACH_PORT_NULL:
    print 'Could not open %s' % args[1]
    return

  # Get size of file
  err, amount = f.readable ()

  if err:
    print 'Could not get number of readable bytes'
    return

  # Read
  err, buf = f.read(amount)

  if err:
    print 'Could not read from file %s' % args[1]
    return

  print buf

if __name__ == "__main__":
  main(sys.argv)
