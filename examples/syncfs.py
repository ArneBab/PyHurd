#!/usr/bin/env python
# -*- coding: utf-8 -*-

'''
syncfs.py - User interface to file_syncfs, synchronize filesystems.
Copyright (C) 2009 Anatoly A. Kazantsev

This program is free software; you can redistribute it and/or modify
it under the terms of the GNU General Public License as published by
the Free Software Foundation; either version 2 of the License, or
(at your option) any later version.

This program is distributed in the hope that it will be useful,
but WITHOUT ANY WARRANTY; without even the implied warranty of
MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
GNU General Public License for more details.

You should have received a copy of the GNU General Public LicensODe along
with this program; if not, write to the Free Software Foundation, Inc.,
51 Franklin Street, Fifth Floor, Boston, MA 02110-1301 USA.
'''

import sys

from optparse import OptionParser

from hurd import Port, error

usage = 'Usage: %prog [OPTION...] FILE...'
description = """Force all pending disk writes to be done immediately
The filesystem containing each FILE is synchronized, and its child
filesystems unless --no-children is specified. With no FILE argument
synchronizes the root filesystem."""

parser = OptionParser(usage = usage, description = description)
parser.add_option('-s', '--synchronous', dest = 'synchronous',
                  action = 'store_true', default = False,
                  help = "Wait for completion of all disk writes")

parser.add_option('-c', '--no-children', dest = 'do_children',
                  action = 'store_false', default = True,
                  help = "Do not synchronize child filesystems")

def sync_one (name, port):
  err = port.syncfs(synchronous, do_children) if port else -1

  if err:
    error(1, err, name)

def main ():
  options, args = parser.parse_args()

  global synchronous, do_children
  
  synchronous = options.synchronous
  do_children = options.do_children

  if not len(args):
    sync_one ('/', Port.getcrdir())
  else:
    for arg in args:
      sync_one (arg, Port.lookup(arg, 0))

if __name__ == "__main__":
  main()
