#!/usr/bin/env python
# -*- coding: utf-8 -*-

cdef extern from "stdio.h":
    file_t glibc_file_name_lookup "file_name_lookup" (char * name, int flags, mode_t mode)