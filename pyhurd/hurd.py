#!/usr/bin/env python
# -*- coding: utf-8 -*-

'''
pyHurd - A pytonish GNU/Hurd
'''

__copyright__ = """
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
"""

from _hurd import IO, File, _getdport
from _fcntl import *

class Port(IO, File):
  def __init__ (self, *args, **kwargs):
    IO.__init__(self, *args, **kwargs)

  @staticmethod
  def lookup (filename, flags, mode = 0):
    import _glibc
    port_name = _glibc.file_name_lookup(filename, flags, mode)

    if port_name:
      return Port(port_name = port_name)
    else:
      return None

  @staticmethod
  def getdport (fd):
    port_name = _getdport(fd)

    if port_name:
      return Port(port_name = port_name)
    else:
      return None
