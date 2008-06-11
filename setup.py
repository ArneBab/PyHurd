#!/usr/bin/env python
# -*- coding: utf-8 -*-

# License ?
#   Anatoly A. Kazantsev: I think about 'GPL2 or later' or GPLv3

try:
    import Cython.Compiler.Version
    #Ugly check, but now only this version is supported :-)
    has_cython = Cython.Compiler.Version.version == '0.9.6.14'
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

pyhurd = CythonExtension('pyhurd',
		sources = ['pyhurd/pyhurd.pyx'])

from setuptools import setup

setup(name = 'PyHurd',
      version = '0.0.0a2',
      
      extras_require = {'Cython' : ['Cython == 0.9.6.14']},

      ext_modules = [pyhurd],
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
