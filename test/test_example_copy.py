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

from examples import main

# !!! UNTRIED TEST !!! #

class TestFile (unittest.TestCase):
    file_path1 = '/tmp/test_file1'
    file_path2 = '/tmp/test_file2'
    test_data = 'abcd'

    def test_0_copy_data (self):
        # Write the test data
        f = open(file_path1, "w")
        f.write(test_data)
        f.close()
        # copy the file
        main(["copy.py", file_path1, file_path2])
        # Get the copied data
        f = open(file_path2, "r")
        data = f.read()
        f.close()

        # Check the data
        self.assertEqual (data, test_data, "Data of copied file doesn't match data written into the original file")

