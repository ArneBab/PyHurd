#!/usr/bin/env python
# encoding: utf-8

"""Create a file object, the PyHurdish way.

 Copyright (C) 2008 Free Software Foundation, Inc.

 Written by Anatoly A. Kazatsev <jim-crow@rambler.ru>.

 Distributed under the terms of the GNU General Public License.
 This is distributed "as is".  No warranty is provided at all.

Status: Only read support, yet (coding time restraints). 

"""

import sys

from pyhurd.glibc import file_name_lookup
from pyhurd.fcntl import O_READ
from pyhurd.mach import MACH_PORT_NULL


class file(object): 
    """A file object. It can read and write.

The file objects are in fact created when doing the read or write operation, 

Just instanciating the class only does some preparation, 
but doesn't lock anything. 
"""
    def __init__(self, path):
        self.path = path

    def read(self, length = None):
	"""Read the content of the file.

doctests: 
    >>> f = file("file.py")
    >>> # read the first 10 bytes
    >>> f.read(10)
    '#!/usr/bin'
"""
        f = file_name_lookup(self.path, O_READ, 0)

        if f is MACH_PORT_NULL: 
            raise Exception("File not found: %s") % path

        # get the size of the file
        err, amount = f.readable ()

        if err:
            raise Exception("Could not get number of readable bytes of %s") % path

        # Read the file data
        if length is None: 
            err, buff = f.read(amount)
        else: 
            err, buff = f.read(length)

        if err:
            raise Exception('Could not read from file %s') % args[1]

        return buff

### Self-Test ###

def _test():
    from doctest import testmod
    testmod()

if __name__ == "__main__":
  _test()
