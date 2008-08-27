#!/usr/bin/env python
# -*- coding: utf-8 -*-

'''
PyHurd - A pytonish GNU/Hurd
'''

cdef extern from "gnu_source.h":
    pass

include "stdlib.pxi"

cdef extern  from "hurd/hurd_types.h":
    ctypedef unsigned int file_t
    ctypedef unsigned int io_t
    ctypedef char * data_t

cdef extern  from "hurd.h":
    ctypedef long loff_t
    ctypedef int pid_t

from pyhurd.mach cimport MachPort

cdef class IO (MachPort):
    cdef readonly io_t io_object

