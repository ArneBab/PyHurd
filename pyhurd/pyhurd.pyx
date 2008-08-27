#!/usr/bin/python
# -*- coding: utf-8 -*-

'''
A pyhurd project
'''

cdef extern from "gnu_source.h":
    pass

cdef extern from "stdlib.h":
    ctypedef unsigned int size_t
    void * malloc (size_t size)

cdef extern from "fcntl.h":
    ctypedef enum:
        _O_READ "O_READ"
        _O_WRITE "O_WRITE"
        _O_CREAT "O_CREAT"
        _O_TRUNC "O_TRUNC"

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

cdef extern  from "hurd/io.h":
    kern_return_t io_readable (io_t io_object, vm_size_t * amount)
    kern_return_t io_read(io_t io_object, data_t * data, mach_msg_type_number_t * dataCnt, loff_t offset, vm_size_t amount)
    kern_return_t io_write(io_t io_object, data_t data, mach_msg_type_number_t dataCnt, loff_t offset, vm_size_t * amount)
    

cdef class IO:
    cdef readonly mach_port_t io_object
    
    def __new__(self):
        self.io_object = _MACH_PORT_NULL

    def __dealloc__(self):
        mach_port_deallocate(mach_task_self(), self.io_object)

    def __str__(self):
        return 'IO: mach port: %s' % self.io_object

    def readable(self):
        cdef vm_size_t amount = 0
        error = io_readable(self.io_object, &amount)
        return error, amount

    def read(self, amount, offset = 0):
        cdef vm_size_t read_amount
        cdef data_t data = <data_t>malloc(amount + 1)
        error = io_read(self.io_object, &data, &read_amount, offset, amount)

        if read_amount == 0:
            return None

        data[read_amount] = c'\0'
        return error, data

    def write(self, data, offset = 0):
        cdef vm_size_t write_amount
        error = io_write(self.io_object, data, len(data), offset, &write_amount)
        return error, write_amount

cdef extern from "stdio.h":
    file_t glibc_file_name_lookup "file_name_lookup" (char *name, int flags, mode_t mode)

def file_name_lookup(filename, flags, mode):
    io_object = glibc_file_name_lookup(filename, flags, mode)

    if io_object == _MACH_PORT_NULL:
        return None

    cdef IO io = IO()
    io.io_object = io_object

    return io

MACH_PORT_NULL = None

O_READ = _O_READ
O_WRITE = _O_WRITE
O_CREAT = _O_CREAT
O_TRUNC = _O_TRUNC

