#!/usr/bin/env python
# -*- coding: utf-8 -*-

import unittest
from test_io import TestIO

if __name__ == '__main__':
    suite_page = unittest.makeSuite(TestIO)
    suite_all = unittest.TestSuite()
    suite_all.addTest(suite_page)

    unittest.TextTestRunner(verbosity=3).run(suite_all)
