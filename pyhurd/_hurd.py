#!/usr/bin/env python
# -*- coding: utf-8 -*-

'''
pyHurd - A pytonish GNU/Hurd
'''

__copyright__ = '''
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

import cython

from _mach import MACH_PORT_NULL

FS_RETRY_NORMAL = _FS_RETRY_NORMAL
FS_RETRY_REAUTH = _FS_RETRY_REAUTH
FS_RETRY_MAGICAL = _FS_RETRY_MAGICAL

INIT_PORT_CWDIR = _INIT_PORT_CWDIR
INIT_PORT_CRDIR = _INIT_PORT_CRDIR
INIT_PORT_AUTH = _INIT_PORT_AUTH
INIT_PORT_PROC = _INIT_PORT_PROC
INIT_PORT_CTTYID = _INIT_PORT_CTTYID
INIT_PORT_BOOTSTRAP = _INIT_PORT_BOOTSTRAP
INIT_PORT_MAX = _INIT_PORT_MAX

@cython.locals(port_name=io_t)
def _getdport(fd):
  port_name = getdport(fd)

  if port_name == _MACH_PORT_NULL:
    return MACH_PORT_NULL
  else:
    return port_name

class Auth:
  @cython.locals (newport = mach_port_t)
  def user_authenticate (self, rendezvous, rendezvousPoly):
    error = auth_user_authenticate (self.mach_port, rendezvous.mach_port, rendezvousPoly, cython.address(newport))
    from hurd import Port
    return error, Port(port_name = newport)

class IO:
  def __init__ (self, *args, **kwargs):
    MachPort.__init__(self, *args, **kwargs)

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
  def seek (self, offset, whence=0):
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

    from hurd import Port
    return error, Port(port_name = _async_id_port)

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

  def reauthenticate (self, rendezvous2, rendevous2Poly):
    return io_reauthenticate (self.mach_port, rendezvous2.mach_port, rendevous2Poly)

class File:
  def chown (self, uid, gid):
    return file_chown (self.mach_port, uid, gid)

  def chauthor (self, new_author):
    return file_chauthor (self.mach_port, new_author)

  def chmod (self, new_mode):
    return file_chmod (self.mach_port, new_mode)

  @cython.locals (data=data_t, size=mach_msg_type_number_t)
  def get_translator (self):
    size = 1025 * cython.sizeof (char)
    data = <data_t>malloc (size)

    error = file_get_translator (self.mach_port, cython.address(data), cython.address(size))

    data[size] = c'\0'

    return error, data

  def syncfs (self, wait, do_children):
    return file_syncfs (self.mach_port, int(wait), int(do_children))

  def set_translator (self, passive_flags, active_flags, oldtrans_flags, passive, active, activePoly):
    return file_set_translator (self.mach_port, passive_flags, active_flags, oldtrans_flags, passive, len(passive), active.mach_port, activePoly)

class Fsys:
  @cython.locals (_file = mach_port_t, _do_retry = retry_type, _gen_uids = idarray_t, _gen_gids = idarray_t)
  def getroot (self, dotdot_node, dotdot_nodePoly, flags, do_retry, retry_name, file, gen_uids = None, gen_gids = None):
    _file = file.mach_port
    _do_retry = do_retry

    _gen_uids_len = len (gen_uids)
    if gen_uids:
      _gen_uids = <idarray_t>malloc (_gen_uids_len * cython.sizeof (uid_t))

      for x in range (0, _gen_uids_len):
        _gen_uids[x] = gen_uids[x]
    else:
      _gen_uids = NULL
      _gen_uids_len = 0

    _gen_gids_len = len (gen_gids)
    if gen_gids:
      _gen_gids = <idarray_t>malloc (_gen_gids_len * cython.sizeof (uid_t))

      for x in range (0, _gen_gids_len):
        _gen_gids[x] = gen_gids[x]
    else:
      _gen_gids = NULL
      _gen_gids_len = 0

    error = fsys_getroot (self.mach_port,
                          dotdot_node.mach_port,
                          dotdot_nodePoly,
                          _gen_uids,
                          _gen_uids_len,
                          _gen_gids,
                          _gen_gids_len,
                          flags,
                          cython.address(_do_retry),
                          retry_name,
                          cython.address(_file))

    from hurd import Port
    return error, _do_retry, Port(mach_port = _file)
