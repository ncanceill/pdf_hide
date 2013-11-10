#!/usr/bin/python3

from distutils.core import setup

#
#
#
# PDF HIDE
#

#
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program.  If not, see [http://www.gnu.org/licenses/].
#
# Copyright (C) 2013 Nicolas Canceill
#

#
# setup.py
__version__ = "0.0"
#
# This is a Python3 setup script for pdf_hide v0.0
#
# Written by Nicolas Canceill
# Last updated on Nov 10, 2013
# Hosted at https://github.com/ncanceill/pdf_hide
#

setup(name='pdf_hide',
	  version=__version__,
	  description='A steganographic tool for hiding data in PDF files',
	  author='Nicolas Canceill',
	  author_email='nicolas.canceill@ens-cachan.org',
	  maintainer='Nicolas Canceill',
	  maintainer_email='nicolas.canceill@ens-cachan.org',
	  url='https://github.com/ncanceill/pdf_hide',
	  license='GNU Public License v3',
	  packages=['pdfhide'],
	  provides=['pdfhide'],
	  scripts=['pdf_hide']
	  )
