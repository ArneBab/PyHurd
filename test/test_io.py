#!/usr/bin/env python
# -*- coding: utf-8 -*-

import unittest

import pyhurd
from pyhurd import file_name_lookup
from pyhurd import O_READ, O_WRITE, O_CREAT, O_TRUNC

class TestIO (unittest.TestCase):
    file_path = '/tmp/test_io'
    test_data = 'abcd'

    def test_0_full_write(self):
        io = file_name_lookup(self.file_path, O_CREAT | O_WRITE | O_TRUNC, 0644)
        error, amount = io.write(self.test_data)

        self.assertEqual(error, 0, 'Errors while writing test file')
        self.assertEqual(amount, len(self.test_data), 'Writed amount of data and lenght of data is not equal')

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


