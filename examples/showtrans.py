#!/usr/bin/env python
# -*- coding: utf-8 -*-

'''
showtrans.py - show files` passive translator.
Copyright (C) 2008 Anatoly A. Kazantsev

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

import sys, errno, os

from optparse import OptionParser

from hurd import Port, O_NOTRANS
from mach import MACH_PORT_NULL


usage = 'Usage: %prog [OPTION...] FILE...'
description = """Show the passive translator of FILE...
A File argument of `-' prints the translator on the node attached to standart
input.
"""

parser = OptionParser(usage=usage, description=description)
parser.add_option('-p', '--prefix', dest='print_prefix',
                  action='store_true', default=None,
                  help="Always display `FILENAME: ' before translators")

parser.add_option('-P', '--no-prefix', dest='print_prefix',
                  action='store_false',
                  help="Never display `FILENAME: ' before translators")

parser.add_option('-s', '--silent', dest='silent', action='store_true',
                  default=False,
                  help='No output; useful when checking error status')

parser.add_option('-t', '--translated', dest='show_untrans',
                  action='store_false', default=True,
                  help='Only display files that have translators')

def print_node_trans (node, name):
  if node is MACH_PORT_NULL:
    sys.stderr.write('Error: %s\n' % name)
  else:
    error, trans = node.get_translator()

    if not error:
      if not silent:
        if print_prefix:
          print '%s: %s' % (name, trans)
        else:
          print trans

      global status
      status = 0
    elif error == errno.EINVAL:
      if not silent and print_prefix and show_untrans:
        print name
    else:
      sys.stderr.write('Error: %s\n' % name)

def main ():
  options, args = parser.parse_args()

  if len(args) == 0:
    print usage
    print "Try `%s --help' for more information." % sys.argv[0]
    sys.exit()

  global print_prefix, silent, show_untrans, status

  status = 1
  print_prefix = options.print_prefix
  silent = options.silent
  show_untrans = options.show_untrans

  if not print_prefix:
    print_prefix = len(args) > 1;

  for arg in args:
    if arg != '-':
      print_node_trans (Port.lookup(arg, O_NOTRANS), arg)
    else:
      print_node_trans (Port.getdport(0), arg)

  sys.exit(status)

if __name__ == "__main__":
  main()
