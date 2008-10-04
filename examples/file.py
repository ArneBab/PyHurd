#!/usr/bin/env python
# encoding: utf-8

"""Create a file object, the PyHurdish way.

 Copyright (C) 2008 Free Software Foundation, Inc.

 Written by Arne Babenhauserheide <arne_bab@web.de>
 based on code from Anatoly A. Kazatsev <anatoly@gnu.org>.

 Distributed under the terms of the GNU General Public License.
 This is distributed "as is".  No warranty is provided at all.

Status: Only read support, yet (coding time restraints). 

"""

import sys

from pyhurd.glibc import file_name_lookup
from pyhurd.fcntl import O_READ
from pyhurd.mach import MACH_PORT_NULL


class HurdFile(object): 
    """A file object. It can read and write.

The file objects are in fact created when doing the read or write operation, 

Just instanciating the class only does some preparation, 
but doesn't lock anything. 
"""
    def __init__(self, path):
	#: The path to the file. 
        self.path = path
	#: The position of the file pointer in the file. 
	self.position = 0

    def read(self, length = None):
	"""Read the content of the file.

doctests: 
    >>> f = HurdFile("file.py")
    >>> # read the first 10 bytes
    >>> f.read(10)
    '#!/usr/bin'
    
TODO: Add seek (self.position) suppport to the read method! 
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
	
	# Update the file pointer
	if length is None: 
	    self.position += amount
	else: 
	    self.position += length

        return buff

    def write(self, data): 
	"""Write a set of bytes to the file."""
	# First get the mach outfile
	out_file = file_name_lookup (self.path, O_WRITE | O_CREAT | O_TRUNC, 0640)
	
	if out_file == MACH_PORT_NULL:
	    raise Exception('Could not open %s') % self.path
	
	# Write the data
	err, amount = out_file.write (data, self.position)
	
	if err:
	    raise Exception('Could not write to file %s') % self.path
	
	# Update the file pointer
	self.position += amount
	
    def seek(self, offset, whence = 0): 
	"""Set the file pointer to a specific position. 
	
    seek(offset[, whence]) -> None.  Move to new file position.

    Argument offset is a byte count.  Optional argument whence defaults to
    0 (offset from start of file, offset should be >= 0); other values are 1
    (move relative to current position, positive or negative), and 2 (move
    relative to end of file, usually negative, although many platforms allow
    seeking beyond the end of a file).  If the file is opened in text mode,
    only offsets returned by tell() are legal.  Use of other offsets causes
    undefined behavior.
    Note that not all file objects are seekable.
	"""
	# If we want absolute positioning, just replace the position in the file. 
	if whence == 0: 
	    self.position = offset
	# If we want relative positioning, add the offset to the position
	elif whence == 1: 
	    self.position += offset
	elif whence == 2: 
	    # And if we want positioning from the end, first get the file length, then update the position
	    # get the size of the file
	    
	    # Get the filesize
	    err, amount = f.readable ()

	    if err:
		raise Exception("Could not get number of readable bytes of %s") % path
	    
	    # Update the file pointer
	    self.position = amount + offset


def main(args): 
    """Example usage of the HurdFile class.

Read the file, print its contents, write something new, read and print that, write the old stuff again and rad and compare to the old stuff. 

>>> main(["test", "new content"])
"""
    if len(args) != 3: 
	print "Usage: file.py <filepath> <new content>"
    
    # Create a file object
    f = HurdFile(args[1])
    
    # print its current content
    old_content = f.read()
    print old_content
    
    # Write, read and then print new content
    f.write(args[2])
    new_content = f.read()
    print new_content
    
    # Write the old content again. 
    f.write(old_content)
    
    # Compare the old content to the file content
    print old_content == f.read()


### Self-Test ###

def _test():
    from doctest import testmod
    testmod()

if __name__ == "__main__":
    _test()
    # Pass the commandline arguments to main
    from sys import argv
    main(argv)