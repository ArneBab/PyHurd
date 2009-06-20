#!/usr/bin/env python
# -*- coding: utf-8 -*-

'''
pyHurd - A pytonish GNU/Hurd
'''

__copyright__ = """
Copyright (C) 2008, 2009 Anatoly A. Kazantsev

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
"""

import sys, inspect, os

from _hurd import Auth, IO, File, Fsys, _getdport, FS_RETRY_NORMAL, FS_RETRY_REAUTH, FS_RETRY_MAGICAL
from _mach import MACH_PORT_NULL
from _fcntl import *

class Port(IO, File, Fsys, Auth):
  def __init__ (self, *args, **kwargs):
    IO.__init__(self, *args, **kwargs)

  @staticmethod
  def lookup (filename, flags = 0, mode = 0):
    import _glibc
    port_name = _glibc.file_name_lookup(filename, flags, mode)

    return Port(port_name = port_name) if port_name else MACH_PORT_NULL

  @staticmethod
  def getdport (fd):
    port_name = _getdport(fd)

    return Port(port_name = port_name) if port_name else MACH_PORT_NULL

  @staticmethod
  def getcrdir ():
    import _glibc
    port_name = _glibc.getcrdir()

    return Port(port_name = port_name) if port_name else MACH_PORT_NULL

def error (status, errnum, message):
  line = inspect.getframeinfo(inspect.currentframe().f_back)[1]
  error_description = os.strerror(errnum)
  output = '%s:%d: %s\n%s\n' % (sys.argv[0], line, message, error_description)

  sys.stderr.write(output)

  if status:
    sys.exit(status)
