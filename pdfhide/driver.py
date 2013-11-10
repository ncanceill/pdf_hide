#!/usr/bin/python3
import os

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
# pdf_drive.py
__version__ = "0.0"
#
# This is a simple API for handling PDF files based on qpdf
#
# Written by Nicolas Canceill
# Last updated on Nov 10, 2013
# Hosted at https://github.com/ncanceill/pdf_hide
#

#
# This module is a wrapper for QPDF and some system utilities for pdf_hide.
#
# It uses Python's OS system calls to expose the QPDF API.
#

#
#
# PUBLIC API
#
#

# Generates QDF file from PDF file, uncompressing streams if needed
def uncompress(input,output):
	os.system('qpdf '+input+' '+output+' --qdf --stream-data=uncompress')

# Generates fixed QDF  file from damaged QDF file, reconstructing XRef and trailer if needed
def fix(input,output):
	os.system('fix-qdf <'+input+' >'+output)

# Generates PDF file from QDF or PDF file, compressing streams if needed
def compress(input,output):
	os.system('qpdf '+input+' '+output+' --stream-data=compress')

# Removes file
def delete(file):
	os.system('rm '+file)

# Fixes, compresses, and cleans
def fcc(input,output):
	fix(input,input+'.fix')
	delete(input)
	compress(input+'.fix',output)
