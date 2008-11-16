#!/usr/bin/env python
# -*- coding: utf-8 -*-

'''
pyHurd - A pytonish GNU/Hurd
'''

__copyright__ = '''
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

import cython

class IO:
  def __str__ (self):
    return 'IO: mach port: %s' % self.mach_port

  @cython.locals(amount=vm_size_t)
  def readable (self):
    '''
    Checks if io object is readable and return avaiable amount
    of data to read/write

    Return:
      tuple of error and amount integer values
    '''

    error = io_readable(self.mach_port, cython.address(amount))

    return error, amount

  @cython.locals(read_amount=vm_size_t, data=data_t)
  def read (self, amount, offset = 0):
    '''
    Reads data from io object.

    Parameters: offset, amount

    Returns: tuple of error (integer) and data (string),
    None - if nothing to read
    '''

    data = <data_t>malloc(amount + 1)
    error = io_read(self.mach_port, cython.address(data), cython.address(read_amount), offset, amount)

    if read_amount == 0:
      return None

    data[read_amount] = c'\0'
    return error, data

  @cython.locals(write_amount=vm_size_t)
  def write (self, data, offset = 0):
    '''
    Writes data to io object.

    Parameters: data - string to write, offset
    Returns: tuple of error and amount values
    '''

    error = io_write(self.mach_port, data, len(data), offset, cython.address(write_amount))

    return error, write_amount
    
  @cython.locals(new_position=loff_t)
  def seek (self, offset, whence):
    '''
    Change current read/write offset

    Return: tuple of error and new position
    '''

    error = io_seek(self.mach_port, offset, whence, cython.address(new_position))

    return error, new_position

  def set_all_openmodes (self, int newbits):
    '''
    Return: error
    '''

    return io_set_all_openmodes(self.mach_port, newbits)

  @cython.locals(bits=int)
  def get_openmodes (self):
    '''
    Return: error, bits
    '''

    error = io_get_openmodes(self.mach_port, cython.address(bits))
    return error, bits

  def set_some_openmodes (self, bits_to_set):
    '''
    Return: error
    '''

    return io_set_some_openmodes(self.mach_port, bits_to_set)

  def clear_some_openmodes (self, bits_to_clear):
    '''
    Return: error
    '''

    return io_clear_some_openmodes(self.mach_port, bits_to_clear)

  @cython.locals(_async_id_port=mach_port_t)
  def async (self, notify_port, notify_portPoly):
    '''
    This requests that the IO object send SIGIO and SIGURG signals,
    when appropriate, to the designated port using sig_post. A
    port is also returned which will be used as the reference port in
    ending such signals (this is the "async IO ID" port).  The async
    call is cancelled by deleting all refernces to the async_id_port.
    Each call to io_async generates a new ASYNC_ID_PORT.

    Return: error, async_id_port
    '''

    error = io_async(self.mach_port, notify_port.mach_port, notify_portPoly, cython.address(_async_id_port))

    async_id_port = MachPort()
    async_id_port.mach_port = _async_id_port

    return error, async_id_port

  def mod_owner (self, owner):
    '''
    Set the owner of the IO object.  For terminals, this affects
    controlling terminal behavior (see term_become_ctty).  For all
    objects this affects old-style async IO.  Negative values represent
    pgrps. This has nothing to do with the owner of a file (as
    returned by io_stat, and as used for various permission checks by
    filesystems).  An owner of 0 indicates that there is no owner.

    Return: error
    '''

    return io_mod_owner(self.mach_port, owner)

  @cython.locals(owner=pid_t)
  def get_owner (self):
    '''
    Get the owner of the IO object.  For terminals, this affects
    controlling terminal behavior (see term_become_ctty).  For all
    objects this affects old-style async IO.  Negative values represent
    pgrps. This has nothing to do with the owner of a file (as
    returned by io_stat, and as used for various permission checks by
    filesystems).  An owner of 0 indicates that there is no owner.

    Return: error, owner
    '''

    error = io_get_owner(self.mach_port, cython.address(owner))

    return error, owner

  @cython.locals(select_type=int)
  def select (self, reply, timeout, select_type):
    '''
    SELECT_TYPE is the bitwise OR of SELECT_READ, SELECT_WRITE,
    and SELECT_URG. Block until one of the indicated types of
    i/o can be done "quickly", and return the types that are
    then available.

    Return: error, select_type
    '''

    error = io_select(self.mach_port, reply, timeout, cython.address(select_type))

    return error, select_type

  @cython.locals(_stat=io_statbuf_t)
  def stat (self):
    error = io_stat(self.mach_port, cython.address(_stat))

    stat = {'st_fstype'  : _stat.st_fstype,
            'st_fsid'    : _stat.st_fsid,
            'st_ino'     : _stat.st_ino,
            'st_gen'     : _stat.st_gen,
            'st_rdev'    : _stat.st_rdev,
            'st_mode'    : _stat.st_mode,
            'st_nlink'   : _stat.st_nlink,
            'st_uid'     : _stat.st_uid,
            'st_gid'     : _stat.st_gid,
            'st_size'    : _stat.st_size,
            'st_atime'   : _stat.st_atime,
            'st_mtime'   : _stat.st_mtime,
            'st_ctime'   : _stat.st_ctime,
            'st_blksize' : _stat.st_blksize,
            'st_blocks'  : _stat.st_blocks,
            'st_author'  : _stat.st_author,
            'st_flags'   : _stat.st_flags }

    return error, stat
