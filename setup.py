#!/usr/bin/env python
# -*- coding: utf-8 -*-

# License ?
#   Anatoly A. Kazantsev: I think about 'GPL2 or later' or GPLv3

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
      version = '0.0.0a3',
      
      #Actually we support 0.9.6.14 release, but this version scheme is no supported by setuptools 
      extras_require = {'Cython' : ['Cython >= 0.9.8']},

      ext_modules = [hurd, mach, glibc, fcntl],
      cmdclass = {'build_ext' : build_ext},

      test_suite = 'test',

      description = 'Pytonish GNU/Hurd',
      author = 'Anatoly A. Kazantsev',
      author_email = 'jim-crow@rambler.ru',

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
