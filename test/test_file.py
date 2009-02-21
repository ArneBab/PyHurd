#!/usr/bin/env python
# -*- coding: utf-8 -*-

'''
pyHurd - A pytonish GNU/Hurd
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
'''

import unittest

from hurd import Port, O_NOTRANS, O_WRITE, O_CREAT, O_TRUNC, O_READ

class TestFile (unittest.TestCase):
    file_path = '/tmp/test_file'
    test_data = 'abcd'

    Port.lookup (file_path, O_WRITE | O_CREAT | O_TRUNC, 0644).write(test_data)

    def test_0_get_translator(self):
	file = Port.lookup ('/proc', O_NOTRANS)
        error, translator = file.get_translator()

        self.assertEqual(error, 0, 'Errors while getting translator for file')
        self.assertEqual(translator, '/hurd/procfs', 'Wrong translator for /proc')

    def test_1_chown(self):
        #TODO
        #file = Port.lookup (self.file_path, O_READ)
        #print file.chown(1000, 1000)
        #print file.stat()
        pass
