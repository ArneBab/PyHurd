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
  ctypedef unsigned int auth_t
  ctypedef unsigned int file_t
  ctypedef unsigned int fsys_t
  ctypedef unsigned int io_t

  ctypedef char * data_t
  ctypedef unsigned int * idarray_t
  ctypedef char string_t [1024]

  ctypedef enum retry_type:
    _FS_RETRY_NORMAL "FS_RETRY_NORMAL" = 1
    _FS_RETRY_REAUTH "FS_RETRY_REAUTH" = 2
    _FS_RETRY_MAGICAL "FS_RETRY_MAGICAL" = 3

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
  io_t getdport(int fd)

from _mach cimport MachPort, kern_return_t, vm_size_t, mach_msg_type_number_t, mach_port_t, mach_msg_type_name_t, natural_t, _MACH_PORT_NULL

cdef extern from 'hurd/auth.h':
  kern_return_t auth_user_authenticate (auth_t handle,
                                        mach_port_t rendezvous,
                                        mach_msg_type_name_t rendezvousPoly,
                                        mach_port_t * newport)

cdef class Auth (MachPort):
  pass


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
  kern_return_t io_reauthenticate (io_t auth_object, mach_port_t rendezvous2, mach_msg_type_name_t rendevous2Poly)

cdef class IO (MachPort):
  pass

cdef extern from "hurd/fs.h":
  kern_return_t file_chown (file_t chown_file, uid_t new_owner, gid_t new_group)
  kern_return_t file_chauthor (file_t chauth_file, uid_t new_author)
  kern_return_t file_chmod (file_t chmod_file, mode_t new_mode)
  kern_return_t file_get_translator (file_t file, data_t *translator, mach_msg_type_number_t * translator_size)
  kern_return_t file_syncfs (file_t file, int wait, int do_children)
  kern_return_t file_set_translator (file_t file, int passive_flags, int active_flags, int oldtrans_flags, data_t passive, mach_msg_type_number_t passiveCnt, mach_port_t active, mach_msg_type_name_t activePoly)

cdef class File (MachPort):
  pass

cdef extern from "hurd/fsys.h":
  kern_return_t fsys_getroot (fsys_t fsys, mach_port_t dotdot_node, mach_msg_type_name_t dotdot_nodePoly, idarray_t gen_uids, mach_msg_type_number_t gen_uidsCnt, idarray_t gen_gids, mach_msg_type_number_t gen_gidsCnt, int flags, retry_type *do_retry, string_t retry_name, mach_port_t *file)

cdef class Fsys (MachPort):
  pass
