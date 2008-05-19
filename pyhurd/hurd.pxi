#!/usr/bin/env python
# -*- coding: utf-8 -*-

cdef extern  from "hurd.h":
    ctypedef unsigned short mode_t
    ctypedef unsigned int mach_port_t
    ctypedef unsigned int file_t
    ctypedef int kern_return_t
    ctypedef unsigned int io_t
    ctypedef unsigned int vm_size_t
    ctypedef unsigned int ipc_space_t
    ctypedef char * data_t
    ctypedef unsigned int mach_msg_type_number_t
    ctypedef long loff_t
    
    ctypedef enum:
        _MACH_PORT_NULL "MACH_PORT_NULL"

    kern_return_t mach_port_deallocate(ipc_space_t space, mach_port_t name)
    mach_port_t mach_task_self()