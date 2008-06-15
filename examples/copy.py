#!/usr/bin/env python
# -*- coding: utf-8 -*-

'''
 copy.py - Copy a file in a "pyhurdish" way.

 Copyright (C) 2008 Free Software Foundation, Inc.

 Written by Anatoly A. Kazatsev <jim-crow@rambler.ru>.

 Distributed under the terms of the GNU General Public License.
 This is distributed "as is".  No warranty is provided at all.
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

