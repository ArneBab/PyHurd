#!/usr/bin/env python
# -*- coding: utf-8 -*-

from pyhurd.hurd cimport file_t, IO
from pyhurd.mach cimport mode_t, _MACH_PORT_NULL

from pyhurd.mach import MACH_PORT_NULL

cdef extern from "stdio.h":
    file_t glibc_file_name_lookup "file_name_lookup" (char * name, int flags, mode_t mode)

def file_name_lookup(filename, flags, mode = 0):
    port = glibc_file_name_lookup(filename, flags, mode)

    if port == _MACH_PORT_NULL:
        return MACH_PORT_NULL

    cdef IO io = IO()
    io.mach_port = port

    return io
