#!/usr/bin/env python
# -*- coding: utf-8 -*-

'''
PyHurd - A pytonish GNU/Hurd
'''

__copyright__ = """
    Copyright © 2008 Anatoly A. Kazantsev <jim-crow@rambler.ru>

    This file is part of PyHurd.

    PyHurd is free software: you can redistribute it and/or modify
    it under the terms of the GNU General Public License as published by
    the Free Software Foundation, either version 3 of the License, or
    (at your option) any later version.

    PyHurd is distributed in the hope that it will be useful,
    but WITHOUT ANY WARRANTY; without even the implied warranty of
    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
    GNU General Public License for more details.

    You should have received a copy of the GNU General Public License
    along with Foobar.  If not, see <http://www.gnu.org/licenses/>.
"""

from pyhurd.hurd cimport file_t, IO
from pyhurd.mach cimport mode_t, _MACH_PORT_NULL

from pyhurd.mach import MACH_PORT_NULL

cdef extern from "stdio.h":
    file_t glibc_file_name_lookup "file_name_lookup" (char * name, int flags, mode_t mode)

def file_name_lookup(filename, flags, mode = 0):
    port = glibc_file_name_lookup(filename, flags, mode)

    if port == _MACH_PORT_NULL:
        return MACH_PORT_NULL

    cdef IO io = IO()
    io.mach_port = port

    return io
