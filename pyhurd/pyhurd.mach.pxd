#!/usr/bin/env python
# -*- coding: utf-8 -*-

cdef extern from "gnu_source.h":
    pass

cdef extern from "mach/port.h":
    ctypedef unsigned int mach_port_t
    ctypedef enum:
        _MACH_PORT_NULL "MACH_PORT_NULL"

cdef extern from "mach/message.h":
    ctypedef unsigned int mach_msg_type_name_t
    ctypedef unsigned int mach_msg_type_number_t

cdef extern from "mach/mach_traps.h":
    mach_port_t mach_task_self()

cdef extern  from "mach/mach_types.h":
    ctypedef unsigned int ipc_space_t

cdef extern  from "mach/error.h":
    ctypedef int kern_return_t

cdef extern from "mach.h":
    ctypedef unsigned short mode_t
    kern_return_t mach_port_deallocate(ipc_space_t space, mach_port_t name)

cdef extern  from "mach/machine/vm_types.h":
    ctypedef unsigned int vm_size_t
    ctypedef unsigned int natural_t

cdef class MachPort:
     cdef readonly mach_port_t mach_port
