#!/usr/bin/env python
# -*- coding: utf-8 -*-

'''
pyHurd - A pytonish GNU/Hurd
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

import unittest

from hurd import Port, O_WRITE, O_CREAT, O_TRUNC

class TestHurd (unittest.TestCase):
    file_name = '/tmp/test_hurd'
    test_data = 'abcd'

    def test_0_getdport(self):
	Port.lookup (self.file_name, O_WRITE | O_CREAT | O_TRUNC, 0644).write(self.test_data)
	
	py_file = open(self.file_name, 'r')
	fd = py_file.fileno()
	
	file = Port.getdport(fd)
	
	self.assertNotEqual(file, None, 'Errors while getting port for file descriptor')
	
	error, data = file.read(4)
	
	py_file.close()

        self.assertEqual(error, 0, 'Errors while reading data from file')
        self.assertEqual(self.test_data, data, 'Wrong read data. Got %s, but should be %s' % (data, self.test_data))
