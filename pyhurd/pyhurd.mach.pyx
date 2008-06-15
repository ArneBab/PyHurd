#!/usr/bin/env python
# -*- coding: utf-8 -*-

MACH_PORT_NULL = None

cdef class MachPort:
    def __new__ (self):
       self.mach_port = _MACH_PORT_NULL

    def __dealloc__ (self):
       mach_port_deallocate(mach_task_self(), self.mach_port)
       
