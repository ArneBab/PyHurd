#!/usr/bin/env python
# -*- coding: utf-8 -*-

from pyhurd.mach cimport mach_port_t

cdef extern  from "hurd/hurd_types.h":
    ctypedef unsigned int file_t
    ctypedef unsigned int io_t
    ctypedef char * data_t

cdef extern  from "hurd.h":
    ctypedef long loff_t
    ctypedef int pid_t

