#!/usr/bin/env python
# -*- coding: utf-8 -*-

from distutils.core import setup, Extension
from Cython.Distutils import build_ext

pyhurd = Extension('pyhurd',
		sources = ['pyhurd/pyhurd.pyx'])

setup(name = 'PyHurd',
      version = '0.0.0a1',
      description = 'Pytonish GNU/Hurd',
      author = 'Anatoly A. Kazantsev',
      author_email = 'jim-crow@rambler.ru',
      ext_modules = [pyhurd],
      cmdclass = {'build_ext' : build_ext})
