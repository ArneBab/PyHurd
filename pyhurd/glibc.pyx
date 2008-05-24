#!/usr/bin/env python
# -*- coding: utf-8 -*-

include "glibc.pxi"

def file_name_lookup(filename, flags, mode = 0):
    io_object = glibc_file_name_lookup(filename, flags, mode)

    if io_object == _MACH_PORT_NULL:
        return None

    cdef IO io = IO()
    io.io_object = io_object

    return io
