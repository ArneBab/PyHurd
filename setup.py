#!/usr/bin/env python
# -*- coding: utf-8 -*-

# License ?

from distutils.core import setup, Extension

try:
    from Cython.Distutils import build_ext
except (Exception):
    print 'You need to install Cython'

pyhurd = Extension('pyhurd',
		sources = ['pyhurd/pyhurd.pyx'])

setup(name = 'PyHurd',
      version = '0.0.0a1',
      description = 'Pytonish GNU/Hurd',
      author = 'Anatoly A. Kazantsev',
      author_email = 'jim-crow@rambler.ru',
      ext_modules = [pyhurd],
      requires = ['Cython (>=0.9.6)'], 
      cmdclass = {'build_ext' : build_ext})

