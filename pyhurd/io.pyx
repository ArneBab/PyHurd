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

    def set_all_openmodes (self, int newbits):
        """
        Return:
             error
        """
        return io_set_all_openmodes(self.io_object, newbits)

    def get_openmodes (self):
        """
        Return:
             error, bits
        """

        cdef int bits
        error = io_get_openmodes(self.io_object, &bits)
        return error, bits

    def set_some_openmodes (self, bits_to_set):
        """
        Return:
             error
        """

        return io_set_some_openmodes(self.io_object, bits_to_set)

    def clear_some_openmodes (self, bits_to_clear):
        """
        Return:
             error
        """

        return io_clear_some_openmodes(self.io_object, bits_to_clear)

    #Looks like we need some sort of MACH_PORT object :-)
    def async (self, notify_port, notify_portPoly):
        """
        This requests that the IO object send SIGIO and SIGURG signals,
        when appropriate, to the designated port using sig_post.  A
        port is also returned which will be used as the reference port in
        sending such signals (this is the "async IO ID" port).  The async
        call is cancelled by deleting all refernces to the async_id_port.
        Each call to io_async generates a new ASYNC_ID_PORT.

        Return:
             error, async_id_port
        """

        cdef mach_port_t async_id_port
        error = io_async(self.io_object, notify_port, notify_portPoly, &async_id_port)
        return error, async_id_port

    def mod_owner (self, owner):
        """
        Set the owner of the IO object.  For terminals, this affects
        controlling terminal behavior (see term_become_ctty).  For all
        objects this affects old-style async IO.  Negative values represent
        pgrps.  This has nothing to do with the owner of a file (as
        returned by io_stat, and as used for various permission checks by
        filesystems).  An owner of 0 indicates that there is no owner.

        Return:
             error
        """

        return io_mod_owner(self.io_object, owner)

    def get_owner (self):
        """
        Get the owner of the IO object.  For terminals, this affects
        controlling terminal behavior (see term_become_ctty).  For all
        objects this affects old-style async IO.  Negative values represent
        pgrps.  This has nothing to do with the owner of a file (as
        returned by io_stat, and as used for various permission checks by
        filesystems).  An owner of 0 indicates that there is no owner.

        Return:
             error, owner
        """

        cdef pid_t owner
        error = io_get_owner(self.io_object, &owner)
        return error, owner

    def select (self, reply, timeout, select_type):
        """
        SELECT_TYPE is the bitwise OR of SELECT_READ, SELECT_WRITE, and SELECT_URG.
        Block until one of the indicated types of i/o can be done "quickly", and
        return the types that are then available.

        Return:
            error, select_type
        """

        cdef int _select_type = select_type
        error = io_select(self.io_object, reply, timeout, &_select_type)
        return error, _select_type
