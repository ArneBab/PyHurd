#!/usr/bin/env python
# -*- coding: utf-8 -*-

cdef extern from "stdlib.h":
    ctypedef unsigned int size_t
    void * malloc (size_t size)