#!/usr/bin/env python
# -*- coding: utf-8 -*-

'''
PyHurd - A pytonish GNU/Hurd
'''

cdef extern from "gnu_source.h":
    pass

include "stdlib.pxi"
include "hurd.pxi"

include "io.pyx"
include "glibc.pyx"

MACH_PORT_NULL = None

