#!/usr/bin/env python
# -*- coding: utf-8 -*-

'''
 dump.py - Dump a file to stdout in a "pyhurdish" way.

 Copyright (C) 2008 Free Software Foundation, Inc.

 Written by Anatoly A. Kazatsev <jim-crow@rambler.ru>.

 Distributed under the terms of the GNU General Public License.
 This is distributed "as is".  No warranty is provided at all.
'''

import sys

from pyhurd import file_name_lookup
from pyhurd import O_READ

def main (args):

  if not len (args) == 2:
    print 'Usage: %s <filename>' % args[0]
    return

  # Open file
  f = file_name_lookup (args[1], O_READ, 0)

  if f is None:
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
