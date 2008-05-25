#!/usr/bin/env python
# -*- coding: utf-8 -*-

cdef extern  from "hurd/io.h":
    kern_return_t io_readable (io_t io_object, vm_size_t * amount)
    kern_return_t io_read (io_t io_object, data_t * data, mach_msg_type_number_t * dataCnt, loff_t offset, vm_size_t amount)
    kern_return_t io_write (io_t io_object, data_t data, mach_msg_type_number_t dataCnt, loff_t offset, vm_size_t * amount)
    kern_return_t io_seek (io_t io_object, loff_t offset, int whence, loff_t * newp)
    kern_return_t io_set_all_openmodes (io_t io_object, int newbits)
    kern_return_t io_get_openmodes (io_t io_object, int * bits)
    kern_return_t io_set_some_openmodes (io_t io_object, int bits_to_set)
