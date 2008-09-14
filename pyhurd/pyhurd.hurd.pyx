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

cdef extern from "gnu_source.h":
    pass

include "stdlib.pxi"

#IO Object
include "io.pyx"

