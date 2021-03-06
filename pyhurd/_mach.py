#!/usr/bin/env python
# -*- coding: utf-8 -*-

'''
pyHurd - A pytonish GNU/Hurd
'''

__copyright__ = """
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
"""

import cython

MACH_PORT_NULL = None

MACH_MSG_TYPE_MOVE_RECEIVE = _MACH_MSG_TYPE_MOVE_RECEIVE
MACH_MSG_TYPE_MOVE_SEND = _MACH_MSG_TYPE_MOVE_SEND
MACH_MSG_TYPE_MOVE_SEND_ONCE  = _MACH_MSG_TYPE_MOVE_SEND_ONCE
MACH_MSG_TYPE_COPY_SEND = _MACH_MSG_TYPE_COPY_SEND
MACH_MSG_TYPE_MAKE_SEND = _MACH_MSG_TYPE_MAKE_SEND
MACH_MSG_TYPE_MAKE_SEND_ONCE = _MACH_MSG_TYPE_MAKE_SEND_ONCE

class MachPort:
  def __cinit__ (cls, *args, **kwargs):
    cls.mach_port = _MACH_PORT_NULL

  def __init__ (self, port_name = MACH_PORT_NULL):
    if port_name:
      self.mach_port = port_name

  def __str__ (self):
    return 'mach_port: %d' % self.mach_port

  def __dealloc__ (self):
    mach_port_deallocate(mach_task_self(), self.mach_port)

  def destroy (self, space = None):
    return mach_port_destroy (mach_task_self () if None else space, self.mach_port)

  def deallocate (self, space = None):
    return mach_port_deallocate (mach_task_self () if None else space, self.mach_port)

@cython.locals (port_name = mach_port_t)
def mach_reply_port ():
  port_name = _mach_reply_port ()
  return MachPort (port_name) if port_name != _MACH_PORT_NULL else MACH_PORT_NULL
