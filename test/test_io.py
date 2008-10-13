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

from pyhurd.glibc import file_name_lookup
from pyhurd.fcntl import O_READ, O_WRITE, O_CREAT, O_TRUNC

class TestIO (unittest.TestCase):
    file_path = '/tmp/test_io'
    test_data = 'abcd'

    def test_0_full_write(self):
        io = file_name_lookup(self.file_path, O_CREAT | O_WRITE | O_TRUNC, 0644)
        error, amount = io.write(self.test_data)

        self.assertEqual(error, 0, 'Errors while writing test file')
        self.assertEqual(amount, len(self.test_data), 'Written amount of data and length of data is not equal')

    def test_1_full_read(self):
        io = file_name_lookup(self.file_path, O_READ)
        result = io.read(len(self.test_data))

        self.assertNotEqual(result, None, 'Test file can not be empty')

        error, data = result

        self.assertEqual(error, 0, 'Errors while reading test file')
        self.assertEqual(data, self.test_data, 'Can not read "%s" from test file' % self.test_data)

    def test_2_readable(self):
        io = file_name_lookup(self.file_path, O_READ)
        error, amount = io.readable()

        self.assertEqual(error, 0, 'Errors while counting amount of data in test file')
        self.assertEqual(amount, len(self.test_data), 'Amount of data in test file and lenght of data is not equal')

    def test_3_stat(self):
        io = file_name_lookup(self.file_path, O_READ)
        error, stat = io.stat()

        self.assertEqual(error, 0, 'Errors while counting amount of data in test file')

        print 'NOT FINISHED TEST!'
	print 'Stat structure:'
	
	for key in stat:
	    print '%s : %s' % (key, str(stat[key]))
	
        self.assertEqual(stat['st_rdev'], 0, 'File is not recognized as normal file')
        self.assertEqual(stat['st_nlink'], 1, 'Must be only one link to this file, but got %i' % stat['st_nlink'])
        self.assertEqual(stat['st_size'], len(self.test_data), 'Size of file is not equal to length of data')

    def test_4_get_openmodes(self):
	io = file_name_lookup(self.file_path, O_READ)
        error, bits = io.get_openmodes()

	self.assertEqual(error, 0, 'Errors while counting amount of data in test file')
	self.assertEqual(bits, 1, 'Openmode is not equal to 1')
