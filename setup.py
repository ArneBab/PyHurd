#!/usr/bin/env python
# -*- coding: utf-8 -*-

'''
pyHurd - A pytonish GNU/Hurd
Copyright (C) 2008 Anatoly A. Kazantsev

This program is free software; you can redistribute it and/or modify
it under the terms of the GNU General Public License as published by
the Free Software Foundation; either version 2 of the License, or
(at your option) any later version.

This program is distributed in the hope that it will be useful,
but WITHOUT ANY WARRANTY; without even the implied warranty of
MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
GNU General Public License for more details.

You should have received a copy of the GNU General Public License along
with this program; if not, write to the Free Software Foundation, Inc.,
51 Franklin Street, Fifth Floor, Boston, MA 02110-1301 USA.
'''

supported_cython_versions = '0.9.6.14', '0.9.8'

try:
    import Cython.Compiler.Version
    #Ugly check
    has_cython = Cython.Compiler.Version.version in supported_cython_versions
except:
    has_cython = False

if has_cython:
    from Cython.Distutils.build_ext import build_ext
else:
    from setuptools.command.build_ext import build_ext

from distutils.core import Extension

class CythonExtension(Extension):
    def __init__ (self, *args, **kw):
        Extension.__init__(self, *args, **kw)

        if not has_cython:
            s = []
            for f in self.sources:
                if f.endswith('.pyx'):
                    name = f[0 : -4]
                    s.append(name + '.c')
                else:
                    s.append(f)

            self.sources = s

import setuptools
setuptools.Extension = CythonExtension

import sys
if 'distutils.command.build_ext' in sys.modules:
    sys.modules['distutils.command.build_ext'].Extension = Extension

hurd = CythonExtension('pyhurd.hurd',
		sources = ['pyhurd/pyhurd.hurd.pyx'])

mach = CythonExtension('pyhurd.mach',
		sources = ['pyhurd/pyhurd.mach.pyx'])

glibc = CythonExtension('pyhurd.glibc',
		sources = ['pyhurd/pyhurd.glibc.pyx'])

fcntl = CythonExtension('pyhurd.fcntl',
		sources = ['pyhurd/pyhurd.fcntl.pyx'])

from setuptools import setup

setup(name = 'PyHurd',
      version = '0.0.0a4',
      
      #Actually we support 0.9.6.14 release, but this version scheme is no supported by setuptools 
      extras_require = {'Cython' : ['Cython >= 0.9.8']},

      ext_modules = [hurd, mach, glibc, fcntl],
      cmdclass = {'build_ext' : build_ext},

      test_suite = 'test',

      description = 'Pytonish GNU/Hurd',
      long_description = '''
PyHurd is an attempt to create full binding to GNU/Hurd API.
It will include bindings to various GNU/Hurd libraries and
will have ability to create translators with python language.
''',
      author = 'Anatoly A. Kazantsev',
      author_email = 'anatoly@gnu.org',
      classifiers = [
        'Development Status :: 1 - Planning',
        'Environment :: Console',
        'Environment :: Other Environment',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: GNU General Public License (GPL)',
        'Natural Language :: English',
        'Operating System :: POSIX :: GNU Hurd',
        'Programming Language :: Python',
        'Topic :: Software Development :: Libraries :: Python Modules',
        'Topic :: System :: Operating System Kernels :: GNU Hurd' 
      ])
