#!/usr/bin/env python
# -*- coding: utf-8 -*-

'''
pyHurd - A pytonish GNU/Hurd
'''

__copyright__ = """
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
"""

cdef extern from "gnu_source.h":
    pass

include "stdlib.pxd"

cdef extern from "time.h":
    ctypedef long int time_t

cdef extern from "sys/types.h":
    ctypedef unsigned long long int fsid_t
    ctypedef unsigned long int ino_t
    ctypedef long int off_t

cdef extern from "sys/stat.h":
    ctypedef unsigned int dev_t
    ctypedef unsigned int mode_t
    ctypedef unsigned int nlink_t
    ctypedef unsigned int uid_t
    ctypedef unsigned int gid_t
    ctypedef long int blksize_t
    ctypedef long int blkcnt_t

cdef extern  from "hurd/hurd_types.h":
    ctypedef unsigned int file_t
    ctypedef unsigned int io_t
    ctypedef char * data_t

    ctypedef struct io_statbuf_t:
        int st_fstype
        fsid_t st_fsid
        ino_t st_ino
        unsigned int st_gen
        dev_t st_rdev
        mode_t st_mode
        nlink_t st_nlink
        uid_t st_uid
        gid_t st_gid
        off_t st_size
        time_t st_atime
        time_t st_mtime
        time_t st_ctime
        blksize_t st_blksize
        blkcnt_t st_blocks
        uid_t st_author
        unsigned int st_flags

cdef extern  from "hurd.h":
    ctypedef long loff_t
    ctypedef int pid_t

from _mach cimport MachPort, kern_return_t, vm_size_t, mach_msg_type_number_t, mach_port_t, mach_msg_type_name_t, natural_t

cdef extern  from "hurd/io.h":
    kern_return_t io_readable (io_t io_object, vm_size_t * amount)
    kern_return_t io_read (io_t io_object, data_t * data, mach_msg_type_number_t * dataCnt, loff_t offset, vm_size_t amount)
    kern_return_t io_write (io_t io_object, data_t data, mach_msg_type_number_t dataCnt, loff_t offset, vm_size_t * amount)
    kern_return_t io_seek (io_t io_object, loff_t offset, int whence, loff_t * newp)
    kern_return_t io_set_all_openmodes (io_t io_object, int newbits)
    kern_return_t io_get_openmodes (io_t io_object, int * bits)
    kern_return_t io_set_some_openmodes (io_t io_object, int bits_to_set)
    kern_return_t io_clear_some_openmodes (io_t io_object, int bits_to_clear)
    kern_return_t io_async (io_t io_object, mach_port_t notify_port, mach_msg_type_name_t notify_portPoly, mach_port_t * async_id_port)
    kern_return_t io_mod_owner (io_t io_object, pid_t owner)
    kern_return_t io_get_owner (io_t io_object, pid_t * owner)
    kern_return_t io_select (io_t io_object, mach_port_t reply, natural_t timeout, int *select_type)
    kern_return_t io_stat (io_t stat_object, io_statbuf_t *stat_info)

cdef class IO (MachPort):
  pass

cdef extern from "hurd/fs.h":
  kern_return_t file_get_translator (file_t file, data_t *translator, mach_msg_type_number_t * translator_size)

cdef class File (MachPort):
  pass