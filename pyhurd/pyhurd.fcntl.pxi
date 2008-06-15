#!/usr/bin/env python
# -*- coding: utf-8 -*-

cdef extern from "fcntl.h":
    ctypedef enum:
        _O_READ "O_READ"
        _O_WRITE "O_WRITE"
        _O_CREAT "O_CREAT"
        _O_TRUNC "O_TRUNC"