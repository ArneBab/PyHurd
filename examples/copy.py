#!/usr/bin/env python
# -*- coding: utf-8 -*-

'''
copy.py - Copy a file in a "pyhurdish" way.
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

from pyhurd.glibc import *
from pyhurd.hurd import *
from pyhurd.mach import MACH_PORT_NULL
from pyhurd.fcntl import *

BUFLEN = 10 # Arbitrary

def main (args):
  if not len(args) == 3:
    print 'Usage: %s <inputfile> <outputfile>' % args[0]
    return

  # Open files
  in_file = file_name_lookup (args[1], O_READ, 0)

  if in_file == MACH_PORT_NULL:
    print 'Could not open %s' % args[1]
    return

  out_file = file_name_lookup (args[2], O_WRITE | O_CREAT | O_TRUNC, 0640)

  if out_file == MACH_PORT_NULL:
    print 'Could not open %s' % args[2]
    return

  in_offset = out_offset = 0

  # Copy
  while True:

    # Read
    result = in_file.read (BUFLEN, in_offset)

    if result == None:
      break

    err, buf = result

    if err:
      print 'Could not read from file %s' % args[1]
      return

    in_offset += len (buf)

    # Write
    while not buf == '':
      err, amount = out_file.write (buf, out_offset)

      if err:
        print 'Could not write to file %s' % args[2]
        return

      buf = buf[amount : ]
      out_offset += amount

if __name__ == "__main__":
  main(sys.argv)

