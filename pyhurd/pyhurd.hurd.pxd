#!/usr/bin/env python
# -*- coding: utf-8 -*-

'''
PyHurd - A pytonish GNU/Hurd
'''

cdef extern from "gnu_source.h":
    pass

include "stdlib.pxi"

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
        unsigned long int st_atime_usec
        time_t st_mtime
        unsigned long int st_mtime_usec
        time_t st_ctime
        unsigned long int st_ctime_usec
        blksize_t st_blksize
        blkcnt_t st_blocks
        uid_t st_author
        unsigned int st_flags

cdef extern  from "hurd.h":
    ctypedef long loff_t
    ctypedef int pid_t

from pyhurd.mach cimport MachPort

cdef class IO (MachPort):
    pass

