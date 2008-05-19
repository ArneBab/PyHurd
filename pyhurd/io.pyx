#!/usr/bin/env python
# -*- coding: utf-8 -*-

include "fcntl.pxi"
include "io.pxi"

O_READ = _O_READ
O_WRITE = _O_WRITE
O_CREAT = _O_CREAT
O_TRUNC = _O_TRUNC

cdef class IO:
    cdef readonly mach_port_t io_object
    
    def __new__ (self):
        self.io_object = _MACH_PORT_NULL

    def __dealloc__ (self):
        mach_port_deallocate(mach_task_self(), self.io_object)

    def __str__ (self):
        return 'IO: mach port: %s' % self.io_object

    def readable (self):
        """
        Checks if io object is readable and return avaiable amount
        of data to read/write

        Return:
            tuple of error and amount integer values

        Hurd definition:
            kern_return_t io_readable (
                io_t io_object,
                vm_size_t *amount)
        """

        cdef vm_size_t amount = 0
        error = io_readable(self.io_object, &amount)

        return error, amount

    def read (self, amount, offset = 0):
        """
        Reads data from io object.

        Parameters:
            offset
            amount

        Returns:
            tuple of error (integer) and data (string)
            None - if nothing to read

        Hurd definition:
            kern_return_t io_read (
                io_t io_object,
                data_t *data,
                mach_msg_type_number_t *dataCnt,
                loff_t offset,
                vm_size_t amount)
        """

        cdef vm_size_t read_amount
        cdef data_t data = <data_t>malloc(amount + 1)
        error = io_read(self.io_object, &data, &read_amount, offset, amount)

        if read_amount == 0:
            return None

        data[read_amount] = c'\0'
        return error, data

    def write (self, data, offset = 0):
        """
        Writes data to io object.

        Parameters:
            data - string to write
            offset

        Returns:
          tuple of error and amount values

        Hurd definition:
            kern_return_t io_write (
                io_t io_object,
	        data_t data,
	        mach_msg_type_number,
	        loff_t offset,
	        vm_size_t *amount)
        """

        cdef vm_size_t write_amount
        error = io_write(self.io_object, data, len(data), offset, &write_amount)
        return error, write_amount

    def seek (self, offset, whence):
        """
        Change current read/write offset

        Return:
            tuple of error and new position

        Hurd definition:
            kern_return_t io_seek (
                io_t io_object,
                loff_t offset,
                int whence,
                loff_t * newp)
        """

        cdef loff_t new_position
        error = io_seek(self.io_object, offset, whence, &new_position)
        return error, new_position
