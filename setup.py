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

## Cython basics

supported_cython_versions = '0.9.8', '0.10', '0.10.2', '0.10.3'

try:
    import Cython.Compiler.Version
    #Ugly check
    has_cython = Cython.Compiler.Version.version in supported_cython_versions
except:
    has_cython = False

from Cython.Distutils.build_ext import build_ext

from distutils.core import Extension

class CythonExtension(Extension):
    def __init__ (self, *args, **kw):
        Extension.__init__(self, *args, **kw)

        if not has_cython:
            s = []
            for f in self.sources:
                name = f[0 : -len('py')]
                s.append(name + 'c')

            self.sources = s

import setuptools
setuptools.Extension = CythonExtension

import sys
if 'distutils.command.build_ext' in sys.modules:
    sys.modules['distutils.command.build_ext'].Extension = Extension

_hurd = CythonExtension('_hurd',
		sources = ['pyhurd/_hurd.py'])

_mach = CythonExtension('_mach',
		sources = ['pyhurd/_mach.py'])

_glibc = CythonExtension('_glibc',
		sources = ['pyhurd/_glibc.py'])

_fcntl = CythonExtension('_fcntl',
		sources = ['pyhurd/_fcntl.py'])

from setuptools import setup


## Read the NEWS file for the long description. 

def read_changelog():
    """Read and return the Changelog

Ideas: 
    - Read only the last three versions or so. 
"""
    try: 
        f = open("NEWS", "r")
        log = f.read()
        f.close()
    except: 
        log = ""
    return log

__changelog__ = "NEWS: \n\n" + read_changelog()


setup(name = 'PyHurd',
      version = '0.0.0a6',

      extras_require = {'Cython' : ['Cython >= 0.9.8']},

      package_dir = {'' : 'pyhurd'},
      packages = [''],

      py_modules = ['hurd', 'mach'],
      ext_modules = [_fcntl, _mach, _hurd, _glibc],
      cmdclass = {'build_ext' : build_ext},

      test_suite = 'test',

      description = 'Pytonish GNU/Hurd',
      long_description = '''
PyHurd is an attempt to create full Python bindings to the GNU/Hurd API. 
It will include bindings to various GNU/Hurd libraries 
and will have the ability to create translators in Python. 
''' + __changelog__.split('\n\n\n')[0],
      author = 'Anatoly A. Kazantsev',
      author_email = 'anatoly@gnu.org',
      url = 'http://savannah.nongnu.org/projects/pyhurd/',
      download_url = 'http://pypi.python.org/pypi/PyHurd/',
      license = 'GNU GPL2',
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

